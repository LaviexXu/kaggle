from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed, PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFPageInterpreter
import re
import jieba


def read_pdf(filename):
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager(caching=False)
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # 用于匹配非标题短句
    not_title = re.compile(r'^.*。$')
    article = ''
    ref_paper = re.compile(r'^\[\d+\].+')
    not_chinese = re.compile(r'\w+')
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
        # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
        for x in layout:
            # 如果x是水平文本对象的话
            if isinstance(x, LTTextBoxHorizontal):
                text = x.get_text().strip()
                para_end = re.match(not_title, text)
                reference = re.match(ref_paper, text)
                # 去除参考文献
                if reference is not None:
                    break
                if len(text) > 25:
                    article += re.sub(not_chinese, '', text)
                elif para_end is not None:
                    article += re.sub(not_chinese, '', para_end.group(0))
    sentences = article.split('。')
    return sentences


def get_similarity(origin_string, compare_string):
    stopwords = {}.fromkeys([line.rstrip() for line in open('ts/stopwords.txt', encoding='utf-8')])
    origin_string_keywords = []
    for word in jieba.cut(origin_string):
        if word not in stopwords:
            origin_string_keywords.append(word)
    compare_string_keywords = []
    for word in jieba.cut(compare_string):
        if word not in stopwords:
            compare_string_keywords.append(word)
    intersection = 0
    for word in compare_string_keywords:
        if word in origin_string_keywords:
            intersection += 1
    union = len(compare_string_keywords) + len(origin_string_keywords) - intersection
    similarity = intersection/union
    return similarity
