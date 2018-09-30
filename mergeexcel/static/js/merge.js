//判断是否是规定类型的上传文件
function change() {

    files = document.querySelector("#nxls").files;


    if ("" != files) {
        for (var i = 0; i < files.length; i++) {
            var filePath = files[i].name

            var fileType = getFileType(filePath);
            //console.log(fileType);
            //判断上传的附件是否为图片
            if ("xls" != fileType && "xlsx" != fileType) {
                $("#nxls").val("");
                alert(filePath + "文件格式不正确,请上传正确的EXCEL文件");
                break;
            }
        }
    }


}

//获取文件类型。
function getFileType(filePath) {
    var startIndex = filePath.lastIndexOf(".");
    if (startIndex != -1)
        return filePath.substring(startIndex + 1, filePath.length).toLowerCase();
    else return "";
}

//定义状态变量。当有文件上传的时候，tim改为1，在下载的时候会判断tim。0为没有上传过文件。1为上传过文件。
var tim = 0

//上传文件函数，ajax实现
function uploads() {
    tim = 1
    $("#a").show();
    $("#s").hide();
    var formData = new FormData();
    var data = document.getElementById("nxls").files;
    for (var i = 0; i < data.length; i++) {
        formData.append("xls", data[i]);
    }
    if (data == undefined) {
        alert("请选择文件上传");
    }
    else {

        $("#xls").val("")
        $.ajax({
            type: 'post',
            url: "/index/upload",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                $(".header").empty();
                var arry = new Array();
                arry = data.header.split("\\");
                $(".header").append("<table id='table'border='1'>");
                for (var i = 1; i < arry.length; i++) {
                    $("#table").append("<td>" + arry[i] + "</td>");
                }
            },
            error: function (data) {
                alert("上传失败");
            },
        });
    }
    $("#a").hide();
    $("#s").show();

}

//排序并导出函数
function download() {

    var data = $("#name").val();
    if (tim == 0) {
        alert("请先上传文件之后，在下载。")
    }
    else {
        //如果用户没有输入排序表头则进入if
        if (data == "") {
            alert("表头排序没有填写，确定按照原始导出嘛？");
            alert("表头排序没有填写，确定按照原始导出嘛？");
            $.ajax(
                {
                    method: "get",
                    url: "/index/sortfile",
                    data: {
                        name: "old"
                    },
                    success: function (res) {
                        if (res.code == 1) {
                            $(".down").html("<a href='/index/download?filename=" + res.url + "'>" + "下载文件" + res.url + "</a>");
                        }
                        else {
                            alert('数据合并失败了，请重试');
                        }
                    },
                    error: function () {
                        alert("请求失败");
                    }
                }
            );
        }
        else {
            $.ajax(
                {
                    method: "get",
                    url: "/index/sortfile",
                    data: {
                        name: data
                    },
                    success: function (res) {
                        if (res.code == 1) {
                            $(".down").html("<a href='/index/download?filename=" + res.url + "'>" + "下载文件" + res.url + "</a>");
                        }
                        else {
                            alert('数据合并失败了，请重试');
                        }
                    },
                    error: function () {
                        alert("请求失败");
                    }
                }
            );
        }
    }
}