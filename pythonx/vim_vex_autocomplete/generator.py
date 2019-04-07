#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
import urllib2
import bs4


_ROOT_URL = 'http://www.sidefx.com/docs/houdini/vex/functions'


def _get_page(url):
    try:
        page = urllib2.urlopen(url)
    except Exception:
        print('Could not load url "{url}"'.format(url=url))
        return None
    return bs4.BeautifulSoup(page, 'html.parser')


def get_all_function_pages():
    page = urllib2.urlopen(_ROOT_URL)
    soup = bs4.BeautifulSoup(page, 'html.parser')

    for function in soup.find_all('li', {'class': 'subtopics_item'}):
        link = function.find('a', href=True)
        url = _ROOT_URL + '/' + link['href']

        function_page = _get_page(url)
        if function_page:
            yield function_page


def get_all_page_signatures(page):
    def _extract_class(signature, class_name):
        unwanted = signature.find('span', {'class': class_name})
        if not unwanted:
            return
        unwanted.extract()

    for signature in page.find_all('code', {'class': 'vexsignature'}):
        # Remove the return type and other things that we don't care about
        _extract_class(signature, 'vexargtype')
        _extract_class(signature, 'vexpattern')
        _extract_class(signature, 'vexrtype')
        _extract_class(signature, 'vextype')

        try:
            yield signature.get_text().encode('utf-8').strip()
        except Exception:
            pass


def main():
    signatures = []
    for page in get_all_function_pages():
        for signature in get_all_page_signatures(page):
            signatures.append('{signature}\t/\tlanguage:vex'.format(signature=signature))
            print(signature)

    print('finished getting signatures')
    with open('/tmp/signatures.tags', 'w') as handler:
        handler.write('\n'.join(signatures))


if __name__ == '__main__':
    main()
