# -*- coding: utf-8 -*-
from .epub_path import EpubPath


class EpubConfig(object):
    u"""
    用于记录epub创建过程中所需用到的常量
    比如，常见模板的实际路径
    """
    base_path = EpubPath.base_path + u'/template'
    # META-INF
    container_uri = base_path + u'/META-INF/container/container.xml'
    duokan_container_uri = base_path + u'/META-INF/duokan_container/duokan-extension.xml'

    # OEBPS

    ## OPF
    opf_content_uri = base_path + u'/OEBPS/opf/content.xml'

    ### guide
    guide_item_uri = base_path + u'/OEBPS/opf/guide/item.xml'

    ### metadata
    metadata_cover_uri = base_path + u'/OEBPS/opf/metadata/cover.xml'
    metadata_creator_uri = base_path + u'/OEBPS/opf/metadata/creator.xml'
    metadata_book_id_uri = base_path + u'/OEBPS/opf/metadata/book_id.xml'
    metadata_title_uri = base_path + u'/OEBPS/opf/metadata/title.xml'

    ### manifest
    manifest_item_uri = base_path + u'/OEBPS/opf/manifest/item.xml'

    ### spine
    spine_item_uri = base_path + u'/OEBPS/opf/spine/item.xml'
    spine_item_nolinear_uri = base_path + u'/OEBPS/opf/spine/item_nolinear.xml'


    ## TOC
    toc_content_uri = base_path + u'/OEBPS/toc/content.xml'
    ###head
    head_uid_uri = base_path + u'/OEBPS/toc/head/uid.xml'
    head_depth_uri = base_path + u'/OEBPS/toc/head/depth.xml'

    # doc_title
    doc_title_title_uri = base_path + u'/OEBPS/toc/docTitle/title.xml'

    ### ncx
    ncx_item_uri = base_path + u'/OEBPS/toc/navMap/item.xml'

    # Directory
    directory_html_uri = base_path + u'/directory/item.html'
    directory_chapter_uri = base_path + u'/directory/chapter.html'
    directory_finish_chapter_uri = base_path + u'/directory/finish_chapter.html'
    directory_content_uri = base_path + u'/directory/content.html'

    # Default
    book_id = u'create_by_yaozeyuan'
    book_title = u'no_title'
    creator = u'zhihuhelp'
    uid = u'urn:uuid:create-by-yao-ze-yuan-Tsingtao'
    identifier = u''
