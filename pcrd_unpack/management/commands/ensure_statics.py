"""
get all static resource from the unpack dir
`force` means replace the file exist in project, note: file in different size will be automatically replaced
"""
from django.core.management.base import BaseCommand, CommandError
import os
import shutil
import distutils
from PIL import Image
import logging
import re
logger = logging.getLogger('django')

class Command(BaseCommand):
    target_static_dir = "pcrd_unpack/static/pcrd_unpack"
    asset_folder = "../unpacked_asset"

    def handle(self, *args, **options):
        self.get_img([
            "Texture2D/assets/_elementsresources/resources/icon/equipment/",
            "Texture2D/assets/_elementsresources/resources/icon/item/",
            "Texture2D/assets/_elementsresources/resources/icon/skill/",
            "Texture2D/assets/_elementsresources/resources/icon/unitplate/",
            "Texture2D/assets/_elementsresources/resources/unit/icon/",
            "Texture2D/assets/_elementsresources/resources/comic/"
        ])
        self.get_img([r"Texture2D\assets\_elementsresources\resources\unit\profile/"], force43=True)
        self.get_img([r"Texture2D\assets\_elementsresources\resources\unit\actualprofile"], force43=True)

    def get_img(self, img_dirs, force43=False, fill_color="#fff", force=False):
        for d_rel in img_dirs:
            d = os.path.join(self.asset_folder, d_rel)
            new_dir = os.path.join(self.target_static_dir, d_rel)
            os.makedirs(os.path.join(new_dir, ""), exist_ok=True)
            # distutils.dir_util.copy_tree(d, new_dir)
            for f in os.listdir(d):
                input_file = os.path.join(d,f)
                outfile = os.path.join(new_dir, f.replace("png", "jpg"))
                if os.path.exists(outfile) and not force :
                    # check if size are the same
                    if os.stat(outfile).st_size == os.stat(input_file).st_size:
                        continue

                im = Image.open(input_file)
                im.convert("RGB")

                if im.mode in ('RGBA', 'LA'):
                    background = Image.new(im.mode[:-1], im.size, fill_color)
                    background.paste(im, im.split()[-1])
                    im = background

                if force43:
                    x, y = im.size
                    y = x // 4 * 3
                    im = im.resize((x, y), Image.ANTIALIAS)
                logger.debug("saved {}".format(outfile))
                im.save(outfile, "JPEG", quality=85)








