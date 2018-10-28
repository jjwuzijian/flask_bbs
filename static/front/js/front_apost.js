$(function () {
    var ue = UE.getEditor("editor",{
        "serverUrl":'/ueditor/upload/'
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();

        var titleInput = $('input[name="title"]');
        var boardselect = $('select[name="board_id"]');
        // var contentInput = $('input[name="content"]');

        var title = titleInput.val();
        var board_id = boardselect.val();
        var content = ue.getContent();

        zlajax.post({
            'url':'/apost/',
            'data':{
                'title':title,
                'content':content,
                'board_id':board_id
            },
            'success':function (data) {
                if(data['code'] == 200){
                    zlalert.alertConfirm({
                        'msg':'恭喜！帖子发表成功！',
                        'cancelText':'回到首页',
                        'confirmText':'再发表一篇',
                        'cancelCallback':function () {
                            window.location = '/';
                        },
                        'confirmCallback':function () {
                            titleInput.val("");
                            ue.setContent("");
                        }
                    });
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});