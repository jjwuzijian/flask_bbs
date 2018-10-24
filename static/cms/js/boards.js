$(function () {
    $("#save-board-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#board-dialog");
        var nameE = $("input[name='name']");

        var name = nameE.val();
        var submitType = self.attr('data-type');
        var boardId = self.attr("data-id");

        if(!name ){
            zlalert.alertInfoToast('请输入完整的板块名称！');
            return;
        }
        var url = '';
        if(submitType == 'update'){
            url = '/cms/uboards/'
        }else {
            url = '/cms/aboards/'
        }

        zlajax.post({
            'url':url,
            'data':{
                'name':name,
                'board_id':boardId,
            },
            'success':function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    window.location.reload();
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail':function (error) {
                zlalert.alertNetworkError();
            }

        });
    });
});

$(function () {
    $(".edit-board-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#board-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");

        var nameE =dialog.find("input[name='name']");
        var saveBtn = dialog.find("#save-board-btn");

        nameE.val(name);
        saveBtn.attr("data-type",'update')
        saveBtn.attr('data-id',tr.attr('data-id'));


    });
});

$(function(){
    $(".delete-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');
        zlalert.alertConfirm({
           'msg':"你确定要删除这个板块吗",
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dboards/',
                    'data':{
                        'board_id':board_id
                    },
            'success':function (data) {
                if(data['code'] == 200){
                    window.location.reload();
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail':function (error) {
                zlalert.alertNetworkError();
            }
                })
            }
        });
    });
});

