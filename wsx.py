#------------------------------------------------------------------------
#                .__                                  __
# __  _  __ ____ |  |   ____  ____   _____   ____   _/  |_  ____
# \ \/ \/ // __ \|  | _/ ___\/  _ \ /     \_/ __ \  \   __\/  _ \
#  \     /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/   |  | (  <_> )
#   \/\_/  \___  >____/\___  >____/|__|_|  /\___  >  |__|  \____/
#              \/          \/            \/     \/
#
#                  __      __  _____________  ___
#                 /  \    /  \/   _____/\   \/  /
#                 \   \/\/   /\_____  \  \     /
#                  \        / /        \ /     \
#                   \__/\  / /_______  //___/\  \
#                        \/          \/       \_/
#
#------------------------------------------------------------------------

import io
import os
import argparse
from StringIO import StringIO
from datetime import datetime
from BeautifulSoup import BeautifulSoup as bs
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
        WebDriverException

from termcolor import cprint


# Settings
#----------------------------------------------------------------------------
msg_color = 'cyan'
err_color = 'red'
success_color = 'green'
t = datetime.now()
screenshots_dir = 'screenshots'
time_format = '%s.%s.%s_%s.%s' % (t.day, t.month, t.year, t.hour, t.minute)
html_file = '%s_web_elements.html' % time_format
#----------------------------------------------------------------------------

def write_html_to_file(filename, html):
    # make BeautifulSoup
    soup = bs(html)
    # prettify the html
    pretty_html = soup.prettify()
    filename.write(pretty_html)


def screenshot_element(im, element):
    """
    :param im: image to crop from
    :param element: web element to crop in image
    :return: cropped image of web element
    """
    size = element.size
    location = element.location

    # cropping the element image
    top = location['y']
    left = location['x']
    bottom = location['y'] + size['height']
    right = location['x'] + size['width']

    # defines crop points
    return im.crop((left, top, right, bottom))


def parse_and_screenshot_xpath_elements(url, xpath,
                                        screenshots=None, htmlfile=None):
    # open driver & connecting to url
    driver = webdriver.Firefox()

    try:
        cprint('[*] Connecting to %s' % url, msg_color)
        driver.get(url)
    except WebDriverException:
        cprint('[!] Target URL %s is not well-formed.' % url, err_color)
        driver.quit()
        return

    try:
        cprint('[*] Scanning for elements that match xpath: %s' % xpath,
                msg_color)
        elements = driver.find_elements_by_xpath(xpath)
        if elements:
            cprint('[*] Found %d matching elements, start parsing\n' %
                    len(elements), success_color)
        else:
            raise Exception("No elements matching xpath: '%s' were found!" %
                            xpath)
    except Exception as e:
        cprint('[!] %s' % e.message, err_color)
        driver.quit()
        return

    # getting screenshot of whole web page
    img = driver.get_screenshot_as_png()
    # open file to write html code to
    f = io.open(htmlfile, mode='ab+')
    # creating directory for screenshots
    if not os.path.exists(screenshots):
        os.makedirs(screenshots)

    for i, e in enumerate(elements,1):
        file_name = 'scr_%s_%d.png' % (time_format, i)
        im = Image.open(StringIO(img))
        im = screenshot_element(im, e)

        print '[*] Element #{n} info:\n' \
              '----------------------\n' \
              '[*] location: {location}\n' \
              '[*] size: {size}'.format(n=i, location=str(e.location),
                                        size=str(e.size)
                                        )

        # saving the image file
        print '[*] Saving screenshot of element #%d to: %s' % (i, file_name)
        im.save(screenshots + '/' + file_name)

        # saving the html code
        print '[*] Saving html code of element #%d to: %s\n' % (i, htmlfile)
        html_code = e.get_attribute('innerHTML')
        write_html_to_file(f, html_code.encode('utf-8'))

    path = os.getcwd() + '/' + screenshots
    cprint('[*] Successfully extracted %d web elements html code to %s' \
          % (i, htmlfile), success_color)
    cprint('[*] Successfully extracted %d web elements images to %s'\
          % (i, path), success_color)
    f.close()
    driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description='Welcome to WSX - Webpage Screenshooter by Xpath - ' \
                    'this utility takes screenshots of web elements matching ' \
                    'given xpath on given url.')

    parser.add_argument('url', help='URL address to take screenshots from',
     type=str, default='https://www.google.com')
    parser.add_argument('-x', '--xpath',
                        help='XPATH of the elements to be screenshoted',
                        type=str, default=".//html")

    parser.add_argument('-s',
                        '--screenshots',
                        help='Folder name where the screennshots of the web' \
                        'elements\' should be saved.',
                        type=str, default=screenshots_dir)

    parser.add_argument('-f',
                        '--html',
                        help='Filename to save web elements\' html code',
                        type=str,
                        default=html_file)

    args = parser.parse_args()
    parse_and_screenshot_xpath_elements(args.url,
                                        args.xpath,
                                        args.screenshots,
                                        args.html)


if __name__ == '__main__':
    main()
