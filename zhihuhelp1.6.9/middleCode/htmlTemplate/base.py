def baseTemplate(dataDict = {}):
    return u"""
            <!DOCTYPE html>
            <html lang="zh-CN">
                <head>
                    <meta charset="utf-8" />
                    <title>{PageTitle}</title>
                </head>
                <body>
                {Guide}
                {Index}
                {Content}
                </body>
            </html>
            """ % dataDict
