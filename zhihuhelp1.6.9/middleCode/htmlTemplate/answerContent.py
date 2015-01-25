def answerContentTemplate(dataDict = {}):
    return u"""
            <div class='answer'>
                <div class='author-info'>
                    <div class='author-logo'>
                    </div>
                    <div class='author-name'>
                    </div>
                    <div class='author-sign'>
                    </div>
                </div>
                <div class='answer-content'>
                </div>
                <div class='answer-info'>
                    <div class='answer-agree'>
                    </div>
                    <div class='answer-comment'>
                    </div>
                    <div class='answer-date'>
                    </div>
                </div>
            </div>
            <hr />
            """ % dataDict
