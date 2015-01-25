def questionContentTemplate(dataDict = {}):
    return u'''
            <div class='question' id='{index}'>
                <div class='question-index'>{index}</div>
                <div class='question-title'>{title}</div>
                <div class='question-desc'>{desc}</div>
                <div class='question-comment'>{comment}</div>
            </div>
            ''' % dataDict

