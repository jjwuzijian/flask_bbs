$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var nameE = $("input[name='name']");
        var imageE = $("input[name='img-url']");
        var linkE = $("input[name='link-url']");
        var priorityE = $("input[name='priority']");

        var name = nameE.val();
        var image_url = imageE.val();
        var link_url = linkE.val();
        var priority = priorityE.val();
        var submitType = self.attr('data-type');
        var bannerId = self.attr("data-id");

        if(!name || !image_url || !link_url || !priority){
            zlalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }
        var url = '';
        if(submitType == 'update'){
            url = '/cms/ubanner/'
        }else {
            url = '/cms/abanner/'
        }

        zlajax.post({
            'url':url,
            'data':{
                'name':name,
                'image_url':image_url,
                'link_url':link_url,
                'priority':priority,
                'banner_id':bannerId,
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
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameE =dialog.find("input[name='name']");
        var imageE = dialog.find("input[name='img-url']");
        var linkE = dialog.find("input[name='link-url']");
        var priorityE = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");

        nameE.val(name);
        imageE.val(image_url);
        linkE.val(link_url);
        priorityE.val(priority);
        saveBtn.attr("data-type",'update')
        saveBtn.attr('data-id',tr.attr('data-id'));


    });
});

$(function(){
    $(".delete-banner-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        zlalert.alertConfirm({
           'msg':"你确定要删除这个轮播图吗",
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dbanner/',
                    'data':{
                        'banner_id':banner_id
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