# -*- coding: utf-8 -*-
from src.tools.path import Path


class EpubConfig(object):
    u"""
    用于记录epub创建过程中所需用到的常量
    比如，常见模板的实际路径
    """

    # META-INF
    container_uri = Path.base_path + '/src/epub/template/META-INF/container/container/container.xml'
    duokan_container_uri = Path.base_path + '/src/epub/template/META-INF/container/duokan_container/duokan-extension.xml'

    # OEBPS

    ## OPF
    opf_content_uri = Path.base_path + '/src/epub/template/OEBPS/opf/content.xml'

    ### guide
    guide_item_uri = Path.base_path + '/src/epub/template/OEBPS/opf/guide/item.xml'

    ### metadata
    metadata_cover_uri = Path.base_path + '/src/epub/template/OEBPS/opf/metadata/cover.xml'
    metadata_creator_uri = Path.base_path + '/src/epub/template/OEBPS/opf/metadata/creator.xml'
    metadata_identifier_uri = Path.base_path + '/src/epub/template/OEBPS/opf/metadata/identifier .xml'
    metadata_title_uri = Path.base_path + '/src/epub/template/OEBPS/opf/metadata/title.xml'

    ### manifest
    manifest_item_uri = Path.base_path + '/src/epub/template/OEBPS/opf/metadata/cover.xml'

    ### spine
    spine_item_uri = Path.base_path + '/src/epub/template/OEBPS/opf/spine/item.xml'
    spine_item_nolinear_uri = Path.base_path + '/src/epub/template/OEBPS/opf/spine/item_nolinear.xml'


    ## TOC
    toc_content_uri = Path.base_path + '/src/epub/template/OEBPS/toc/content.xml'
    ###head
    head_uid_uri = Path.base_path + '/src/epub/template/OEBPS/toc/head/uid.xml'
    head_depth_uri = Path.base_path + '/src/epub/template/OEBPS/toc/head/depth.xml'

    # doc_title
    doc_title_title_uri = Path.base_path + '/src/epub/template/OEBPS/toc/docTitle/title.xml'

    ### ncx
    ncx_item_uri = Path.base_path + '/src/epub/template/OEBPS/toc/navMap/item.xml'
