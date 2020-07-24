

layui.use(['table','form'], function(){
	var $=layui.$;
	var table = layui.table;
	var form=layui.form;
  table.render({
    elem: '#list'
	,data:tabledata
    ,toolbar: '#toolbar' //开启头部工具栏，并为其绑定左侧模板
    ,title: '导出数据表'
    ,cols: [[
		{checkbox: true, fixed: true}
		,{title: '序号',templet: '#xuhao'}
		,{field:"tablename",title:"图表名"}
		,{field:"filename",title:"文件名"}
		,{field:"type",title:"图表类型"}
	   ,{fixed: 'right', title:'操作', toolbar: '#rowbar'}
    ]]
    ,page: true
  });
  //定义增加一行数据的函数
	var addrow=function(tablename,filename,type="柱状图"){
			var oldData=table.cache['list'];
			oldData.push({
				tablename:tablename,
				filename:filename,
				type:type
			})
			table.reload('list',{data:oldData});
		}
			
  //头工具栏事件
  table.on('toolbar(list)', function(obj){
    var checkStatus = table.checkStatus(obj.config.id);
    switch(obj.event){
      case 'addtable':
        //var data = checkStatus.data;
		//处理增加事件
        layer.open({
			type:2,
			content:'static/_form.html',
			title:"增加图表",
			btn:['保存','取消'],
			yes:function(index, layero){
				//获取frame层的表单数据
				var body = layer.getChildFrame('body', index);
				var tablename=body.contents().find("#tablename").val();
				var filename=body.contents().find("#filename").val();
				var type=body.contents().find("#type").val();
				//如果没有文件名就提示
				if(filename=="")
				return(layer.msg("请选择文件！"));
				//处理表单数据
				if(tablename==""){//对于没有tablename的按照批量导入计算
					$.get('/gettablename/'+filename,function(data){
						if(data['code']=="0"){
							$.each(data['data'],function(i,item){
								addrow(item,filename);
								layer.msg("添加成功!");
								layer.close(index);
							})
						}
						else {
							layer.msg(data.msg);
						}
					});
					
				}
				else{//检查是否有tablename
					$.get('/checktablename/'+filename+'/'+tablename,function(data){
						if(data['code']==0){
							addrow(tablename,filename,type);
							layer.msg("添加成功!");
							layer.close(index);
						}
						else{
							layer.msg(data['msg']);
						}
					});
				}
			},
			btn2:function(){

			},
			shadeClose:false,
			area:['500px','600px']


		})
		break;
		case 'importsettings':
			layer.msg("该功能暂未实现");
			break;
		case 'exportsettings':
       
			break;
		case 'rendertable':
		//获取选中行数据
			var Data=table.checkStatus('list').data;
			if(Data.length==0){return layer.msg("请至少选中一条数据！")}
			jsonData=JSON.stringify(Data);
			$.ajax({
				url:"/rendertable",
				type:"POST",
				data:jsonData,
				dataType:'json',
				success:function(data){
					console.log(data);
					if(data['code']!=200){
						layer.confirm(data['msg']);
					}
					else{
						console.log(data['data']);
						var url='/downloads/';
						console.log(url+data['data']['renderfilename']);
						window.location.href=url+data['data']['renderfilename'];
						
					}
				}
			});
			break;
      //自定义头工具栏右侧图标 - 提示
     
    };
  });

  //监听行工具事件
  table.on('tool(list)', function(obj){
	 var data=obj.data;
    if(obj.event === 'del'){
      layer.confirm('真的删除行么', function(index){
        obj.del();
        layer.close(index);
      });
    } else if(obj.event === 'edit'){
		layer.open({
			type:2,
			content:'static/_form.html',
			title:"修改图表",
			btn:['保存','取消'],
			//注意这里参数不要写反了
			yes:function(index, layero){
				//获取frame层的数据
				var body = layer.getChildFrame('body', index);
				var tablename=body.contents().find("#tablename").val();
				var filename=body.contents().find("#filename").val();
				var type=body.contents().find("#type").val();
				
				//处理表单数据
				if(tablename==""){//对于没有tablename的提示
					return(layer.msg("输入sheet名！"));
				}
				else{//检查是否有tablename
					$.get('/checktablename/'+filename+'/'+tablename,function(data){
						if(data['code']==0){
							obj.del();
							addrow(tablename,filename,type);
							layer.msg("修改成功!");
							layer.close(index);
						}
						else{
							layer.msg(data['msg']);
						}
					});
				}
				
			},
			btn2:function(){

			},
			shadeClose:false,
			area:['500px','600px'],
			end:function(){

			},
			//渲染frame层数据
			success:function(layero, index){  //为什么这次变成了layero在前面？？？
				var body = layer.getChildFrame('body', index);
				body.contents().find("#upload").html('<i class="layui-icon">&#xe67c;</i>重新上传');
				body.contents().find("#tablename").val(data["tablename"]);
				body.contents().find("#filename").val(data["filename"]);
				body.contents().find("#type").val(data["type"]);
			}

      });
    }
  });
});