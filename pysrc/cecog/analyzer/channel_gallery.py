"""
channel_gallery.py

make little image galleries for single objects vs. channel

"""

__author__ = 'rudolf.hoefler@gmail.com'
__copyright__ = ('The CellCognition Project'
                 'Copyright (c) 2006 - 2012'
                 'Gerlich Lab, IMBA Vienna, Austria'
                 'see AUTHORS.txt for contributions')
__licence__ = 'LGPL'
__url__ = 'www.cellcognition.org'


from os.path import isdir, join
from matplotlib.colors import hex2color, is_color_like
import numpy as np
import vigra

from cecog.colors import Colors
from cecog.util.util import makedirs


# class GalleryImage(np.ndarray):

#     def __new__(cls, shape, nsub=1, *args, **kw):
#         obj = np.ndarray.__new__(cls, shape, *args, **kw)
#         obj._nsub = nsub
#         return obj

#     def __array_finalize__(self, obj):
#         # np.ndarray.__array_finalze__(self, obj)
#         pass

#     def set_sub_image(self, position, image):
#         width = self.shape[0]/self._nsub
#         xmin = position*width
#         xmax = (position+1)*width
#         self[xmin:xmax] = image


class GalleryRGBImage(np.ndarray):

    def __new__(cls, shape, nsub=1, *args, **kw):
        if len(shape) != 3:
            raise RuntimeError("rgb image need a shape of lenght 3")
        obj = np.ndarray.__new__(cls, shape, *args, **kw)
        obj._nsub = nsub
        return obj

    def __init__(self, *args, **kw):
        super(GalleryRGBImage, self).__init__(*args, **kw)
        self.contours = list()
        self._swidth = None

    def __array_finalize__(self, obj):
        # np.ndarray.__array_finalze__(self, obj)
        pass

    @property
    def swidth(self):
        """Width of a single sub image (column)"""
        if self._swidth is None:
            self._swidth = self.shape[0]/self._nsub
        return self._swidth

    def set_sub_image(self, position, image, color="#FFFFFF"):
        rgb_img = self._grey2rgb(image, color)
        xmin = position*self.swidth
        xmax = (position+1)*self.swidth
        self[xmin:xmax, :, :] = rgb_img

    def _grey2rgb(self, image, color="#FFFFFF"):
        if is_color_like(color):
            color = hex2color(color)
        # be aware that color contains floats ranging from 0 to 1
        return np.dstack((image, image, image))*np.array(color)

    def merge_sub_images(self):
        mimg = np.zeros((self.swidth, self.shape[1], 3))
        for i in xrange(self._nsub-1):
            mimg += self[i*self.swidth:(i+1)*self.swidth, :, :]
        self[(self._nsub-1)*self.swidth:, :, :] = mimg

    def add_contour(self, position, contour, color):
        if is_color_like(color):
            color = hex2color(color)
        color = np.array(color)
        color = np.round(color*np.iinfo(self.dtype).max)

        contour = contour + np.array((0, position*self.swidth))
        # rgb color according to dtype of the image
        self.contours.append((contour[:, 1], contour[:, 0], color))

    def draw_contour(self):
        for ix, iy, color in self.contours:
            self[ix, iy] = color

    def draw_merge_contour(self, color, idx=0):
        if is_color_like(color):
            color = hex2color(color)
        color = np.array(color)
        color = np.round(color*np.iinfo(self.dtype).max)
        ix, iy, _ = self.contours[idx]

        # shift contour from subimage to the last column
        xoff = (self._nsub-1-idx)*self.swidth
        self[ix+xoff, iy] = color


class ChannelGallery(object):

    def __init__(self, channel, frame, outdir, size=200):

        if not channel.is_virtual():
            raise RuntimeError("ChannelGallery need a virtual channel")
        if not isdir(outdir):
            raise RuntimeError("Output directory does not exist")

        self._channel = channel
        self._outdir = outdir

        # want even number
        if size%2:
            size += 1
        self._size = size
        self._frame = frame

    def gallery_name(self, label):
        fname = "T%05d_L%s.png" %(self._frame, label)
        subdir = "-".join(self._channel.merge_regions)
        return join(self._outdir, subdir, fname)

    def _i_sub_image(self, center, (height, width)):
        """Return the pixel indices of the sub image according to the size of
        the gallery."""

        xmin = center[0] - self._size/2
        xmax = center[0] + self._size/2
        ymin = center[1] - self._size/2
        ymax = center[1] + self._size/2

        # range checks
        if xmin < 0:
            xmin, xmax = 0, self._size
        if xmax > width:
            xmin, xmax = width-self._size, width

        if ymin < 0:
            ymin, ymax = 0, self._size
        if ymax > height:
            ymin, ymax = height-self._size, height

        if (xmax - xmin) != (ymax-ymin):
            import pdb; pdb.set_trace()

        return xmin, xmax, ymin, ymax

    def cut(self, image, (xmin, xmax, ymin, ymax)):
        return image[ymin:ymax, xmin:xmax]

    def make_target_dir(self):
        makedirs(join(self._outdir, "-".join(self._channel.merge_regions)))

    def make_gallery(self):
        #  >= 2
        n_ch = len(self._channel.merge_regions)+1
        self.make_target_dir()

        holder = self._channel.get_region(self._channel.regkey)
        for label in holder:
            iname = self.gallery_name(label)
            center = holder[label].oCenterAbs
            gallery = GalleryRGBImage(((n_ch)*self._size, self._size, 3), dtype=np.uint8,
                                   nsub=n_ch)

            for i, (channel, region) in enumerate(self._channel.sub_channels()):
                image = channel.meta_image.image.toArray()
                hexcolor = Colors.channel_hexcolor(channel.strChannelId)
                sholder = channel.get_region(region)
                sample = sholder[label]

                roi = self._i_sub_image(center, image.shape)
                sub_img = self.cut(image, roi)
                gallery.set_sub_image(i, sub_img, hexcolor)

                # draw contour
                contour = np.array(sample.crack_contour) - np.array(sample.oCenterAbs)
                contour += self._size/2
                gallery.add_contour(i, contour, sample.strHexColor)

            # first merged sub images, then draw conturs
            gallery.merge_sub_images()
            gallery.draw_contour()
            gallery.draw_merge_contour(holder[label].strHexColor)

            vigra.RGBImage(gallery).writeImage(iname)
