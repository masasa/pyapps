import os
import argparse
from StringIO import StringIO
from PIL import Image
from selenium import webdriver
from datetime import datetime

screenshots_dir = 'screenshots'


def screenshot_element(im, element):
    """
    :param im: image to crop from
    :param element: web element to crop in image
    :return: cropped image of web element
    """
    size = element.size
    location = element.location

    # cropping the element image
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    # defines crop points
    return im.crop((left, top, right, bottom))


def parse_and_screenshot_xpath_elements(url, xpath=None, screenshots=None):

    # open driver & connecting to url
    driver = webdriver.Firefox()

    print '[*] Connecting to %s' % url
    driver.get(url)

    print '[*] Scanning for elements that match xpath: %s' % xpath

    elements = driver.find_elements_by_xpath(xpath)

    print '[*] Found %d matching elements, start parsing\n' % len(elements)

    # getting screenshot of whole web page
    img = driver.get_screenshot_as_png()

    # creating directory for screenshots
    if not os.path.exists(screenshots):
        os.makedirs(screenshots)

    ecount = 0
    t = datetime.now()
    time_format = '%s.%s.%s_%s.%s' % (t.day, t.month, t.year, t.hour, t.minute)

    for e in elements:
        ecount += 1
        file_name = 'scr_%s_%d.png' % (time_format, ecount)

        im = Image.open(StringIO(img))
        im = screenshot_element(im, e)

        print '[*] Element #{n} info:\n----------------------\nlocation: ' \
              '{location}\nsize: {size}\n'.format(n=ecount,
                                                  location=str(e.location),
                                                  size=str(e.size)
                                                  )

        print '[*] Saving screenshot of element #%d: %s\n' % (ecount,
                                                              file_name)

        # saving the image file
        im.save(screenshots + '/' + file_name)

    path = os.getcwd() + '/' + screenshots
    print '[*] Successfully extracted %d images to %s' % (ecount, path)
    driver.quit()


def main():
    parser = argparse.ArgumentParser(description='Takes screenshots of '
                                                 'elements matching given '
                                                 'xpath on given url.')
    parser.add_argument('url', help='url address', type=str)
    parser.add_argument('-x', '--xpath', help='elements xpath', type=str,
                        default="./*")
    parser.add_argument('-s', '--screenshots', help='folder name to save '
                                                    'screenshots', type=str,
                        default=screenshots_dir)

    args = parser.parse_args()
    parse_and_screenshot_xpath_elements(args.url, args.xpath, args.screenshots)


if __name__ == '__main__':
    main()
