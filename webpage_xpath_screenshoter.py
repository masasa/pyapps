import argparse
import io
import os
from StringIO import StringIO
from datetime import datetime

from BeautifulSoup import BeautifulSoup as bs
from PIL import Image
from selenium import webdriver

screenshots_dir = 'screenshots'
html_file = 'elements.html'


def write_html_to_file(file, html):

    # make BeautifulSoup
    soup = bs(html)

    # prettify the html
    pretty_html = soup.prettify()

    file.write(pretty_html)


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


def parse_and_screenshot_xpath_elements(url,
                                        xpath=None,
                                        screenshots=None,
                                        htmlfile=None):

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

    f = io.open(htmlfile, mode='ab+')

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

        html_code = e.get_attribute('innerHTML')
        write_html_to_file(f, html_code)

        # saving the image file
        im.save(screenshots + '/' + file_name)

    path = os.getcwd() + '/' + screenshots
    print '[*] Successfully extracted %d web elements to %s' % (ecount,
                                                                htmlfile)
    print '[*] Successfully extracted %d images to %s' % (ecount, path)
    f.close()
    driver.quit()


def main():
    parser = argparse.ArgumentParser(description='Takes screenshots of '
                                                 'elements matching given '
                                                 'xpath on given url.')
    parser.add_argument('url', help='url address', type=str)
    parser.add_argument('-x',
                        '--xpath',
                        help='elements xpath',
                        type=str,
                        default="./*")

    parser.add_argument('-s',
                        '--screenshots',
                        help='folder name to save screenshots',
                        type=str,
                        default=screenshots_dir)

    parser.add_argument('-f',
                        '--html',
                        help='file to save html code of xpath elements',
                        type=str,
                        default=html_file)


    args = parser.parse_args()
    parse_and_screenshot_xpath_elements(args.url,
                                        args.xpath,
                                        args.screenshots,
                                        args.html)


if __name__ == '__main__':
    main()
