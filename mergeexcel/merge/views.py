import os
from django.conf import settings
from .utils import *
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
#上传文件函数
def upload(req):
    #如果是post则处理上传的文件
    if req.method == "POST":
        # 获得文件
        f = req.FILES.getlist("xls")
        if len(f) == 1:
            # 获取文件名字
            file_name = f[0].name
            # 拼接文件路径
            file_path = os.path.join(settings.UPLOADFILES, file_name)
            # 打开文件
            with open(file_path, 'wb') as fp:
                # 遍历写入我们的本地文件
                for j in f[0].chunks():
                    fp.write(j)
            #合并文件
            ist = mergerexcel(file_path)
            a = ' \ '
            #拼接
            h = a.join(ist)
            print("表头是：：：：", h)
            if type(ist) == type([]):
                data = {
                    'code': 1,
                    'msg': "ok",
                    'header': h,
                }
                return JsonResponse(data)
            else:
                return HttpResponse("合并时出错，请联系技术员,错误信息是：" + str(ist))
        else:
            #多个文件的时候
            #获取文件，生成列表
            file_names = [i.name for i in f]
            #拼接路径
            file_paths = [os.path.join(settings.UPLOADFILES,i) for i in file_names]
            # 将文件写入本地
            for i in range(len(file_paths)):
                with open(file_paths[i], 'wb') as fp:
                    # 遍历写入我们的本地文件
                    for j in f[i].chunks():
                        fp.write(j)
            #合并文件
            ist = mergerexcels(file_paths)
            a = ' \ '
            h = a.join(ist)
            if type(ist) == type([]):
                data = {
                    'code': 1,
                    'msg': "ok",
                    'header': h,
                }
                return JsonResponse(data)
            else:
                return HttpResponse("合并时出错，请联系技术员,错误信息是：" + str(ist))

    else:
            return render(req, "upload.html")
#按照要求排序
def sortfile(req):
    #获取排序名称
    name = req.GET.get("name")
    #如果是old则表示前端没有输入排序的表头
    if name == "old":
        #路径下的文件
        merge = os.listdir(settings.DOWNLOADFILES)
        #拼接路径
        path = os.path.join(settings.DOWNLOADFILES, merge[0])
        #去重函数
        quchong(merge=path)
        data = {
            'code': 1,
            'msg': "ok",
            'url': merge,
        }
        return JsonResponse(data)

    else:
        #切割用户输入的表头
        namelist =name.split("\\")
        #排序
        if sortexcel(namelist):
            merge = os.listdir(settings.DOWNLOADFILES)
            path = os.path.join(settings.DOWNLOADFILES,merge[0])
            #去重
            quchong(merge=path)
            data = {
                'code': 1,
                'msg': "ok",
                'url': merge,
            }
            return JsonResponse(data)
        else:
            data = {
                'code': 0,
                'msg': "排序出错",
                'url': "",
            }
            return JsonResponse(data)
#下载文件
def download(req):
    try:
        #获取前端传递给的下载文件名称
        download_name = req.GET.get("filename")
        #拼接路径
        filename = os.path.join(settings.DOWNLOADFILES, download_name)
        #获取文件流并生成响应
        response = StreamingHttpResponse(readFile(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(download_name)
        return response
    except Exception as e:
        print(e)
        return response


