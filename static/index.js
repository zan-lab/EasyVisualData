layui.use(['element','table'],function(){
	var element=layui.element;
	var $=layui.$;
	var form=layui.form;
	$(".layui-body").load('static/_main.html');
	
	
	$("#zzt").click(function(){
		$(".layui-body").load('static/_zhuzhuangtu.html');
	})	
	$("#zxt").click(function(){
		$(".layui-body").load('static/_zhexiantu.html');
	})	
	$("#bt").click(function(){
		$(".layui-body").load('static/_bingtu.html');
	})		
	$("#sysm").click(function(){
		$(".layui-body").load('static/_shiyongshuoming.html');
	})		
	$("#main").click(function(){
		$(".layui-body").load('static/_main.html');
	})	
		
		
	
		
		
});
			