$(function() {
	password_login();
	var setting = {
		imageWidth : 1680,
		imageHeight : 1050
	};
	var init = function() {
		var windowHeight = $(window).height();
		var windowWidth = $(window).width();
		$(".login_conatiner").css("height",windowHeight);
		$(".login_conatiner").css("width",windowWidth);
		
		$("#container_bg").css("height",windowHeight);
		$("#container_bg").css("width",windowWidth);
		
		$("#login_right_box").css("height",windowHeight);

		var imgW = setting.imageWidth;
		var imgH = setting.imageHeight;
		var ratio = imgH / imgW; // 图片的高宽比

		imgW = windowWidth; // 图片的宽度等于窗口宽度
		imgH = Math.round(windowWidth * ratio); // 图片高度等于图片宽度 乘以 高宽比

		if (imgH < windowHeight) { // 但如果图片高度小于窗口高度的话
			imgH = windowHeight; // 让图片高度等于窗口高度
			imgW = Math.round(imgH / ratio); // 图片宽度等于图片高度 除以 高宽比
		}

		$(".login_img_01").width(imgW).height(imgH); // 设置图片高度和宽度
	};

	//密码找回的中英文切换
	if($("#change_language").attr("value") == "中文"){
		$("#pwd_url").attr("href",$("#pwd_url").attr("href")+"?locale=en");
	}else{
		$("#pwd_url").attr("href",$("#pwd_url").attr("href")+"?locale=zh_CN");
	}
	$("#change_language").unbind("click").click(function(){
		var re=eval('/(locale=)([^&]*)/gi');
		var url = window.location.href;
		if($("#change_language").attr("value") == "中文"){
			if(url.indexOf("locale") >= 0 ) {
				url=url.replace(re,'locale=zh_CN');
				location.href=url;
			}else{
				if(url.indexOf("?") >= 0){
					location.href=url+"&locale=zh_CN";
				}else{
					location.href=url+"?locale=zh_CN";
				}
			}
		}else if($("#change_language").attr("value") == "English") {
			if(url.indexOf("locale") >= 0 ) {
				url=url.replace(re,'locale=en');
				location.href=url;
			}else{
				if(url.indexOf("?") >= 0){
					location.href=url+"&locale=en";
				}else{
					location.href=url+"?locale=en";
				}
			}
		}
	});
	
	init();
	
	//显示验证码
	//getImageCode();
	
	$(window).resize(function() {
		init();
	});
	

	//如果有错误信息，则显示
	if($("#errormsg").text()){
		$("#errormsg").parent().show();
	}
	
	//触发如何使用360极速模式图片
	$("#open_360").mouseover(function(){
		$("#open_360_img").show();
	}).mouseout(function(){
		$("#open_360_img").hide();
	});
	
	//用户名文本域keyup事件
//	$("#un").keyup(function(e){
//		if(e.which == 13) {
//			login();
//	    }
//	}).keydown(function(e){
//		$(this).parent().removeClass("login_error_border");
//		$("#errormsg").parent().hide();
//	}).focus();
	
	//密码文本域keyup事件
//	$("#pd").keyup(function(e){
//		if(e.which == 13) {
//			login();
//	    }
//	}).keydown(function(e){
//		$(this).parent().removeClass("login_error_border");
//		$("#errormsg").parent().hide();
//	});
	
	$("a[name='login_type']").unbind().bind("click",function(){
		if($(this).attr("type")=='account'&&!$(this).hasClass("active")){
			password_login();
		}
		if($(this).attr("type")=='scan'&&!$(this).hasClass("active")){
			qrcode_login();
			$("#errormsg").parent().hide();
		}
		$(this).addClass("active").siblings().removeClass("active");
	});
});

function password_login(){
	var passwordhtml = document.getElementById("password_template").innerHTML;	
	$("#template_container").html(passwordhtml);
	
	//触发如何使用360极速模式图片
	$("#open_360").mouseover(function(){
		$("#open_360_img").show();
	}).mouseout(function(){
		$("#open_360_img").hide();
	});
	if($("#change_language").attr("value") == "English"){
		$("#tip3").show();
		$("#tip4").show();
	}else{
		$("#tip3").hide();
		$("#tip4").hide();
	}
	//显示验证码
	//getImageCode();
	//重新获取验证码
	$("#a_changeCode").click(function(){
    	$("#codeImage").attr("src", "code?"+Math.random()) ;
    });
	//登录按钮触发
	$("#index_login_btn").click(function(){
		login();
	});
	
	//用户名文本域keyup事件
	$("#un").keyup(function(e){
		if(e.which == 13) {
			login();
	    }
	}).keydown(function(e){
		$(this).parent().removeClass("login_error_border");
		$("#errormsg").parent().hide();
	}).focus();
	
	//密码文本域keyup事件
	$("#pd").keyup(function(e){
		if(e.which == 13) {
			login();
	    }
	}).keydown(function(e){
		$(this).parent().removeClass("login_error_border");
		$("#errormsg").parent().hide();
	});
}

//加载扫码登录功能
function qrcode_login(){
	var qrcodehtml = document.getElementById("qrcode_template").innerHTML;
	$("#template_container").html(qrcodehtml);
	//微信企业号扫码登录 add by TJL
	var lqrcode = new loginQRCode("qrcode",153,153);
	lqrcode.generateLoginQRCode(function(result){
		window.location.href = result.redirect_url;
	});
}

function login(){
	var $u = $("#un") , $p=$("#pd");
	
	var u = $u.val();
	if(u==""){
		$u.focus();
		$u.parent().addClass("login_error_border");
		return ;
	}
	
	var p = $p.val();
	if(p==""){
		$p.focus();
		$p.parent().addClass("login_error_border");
		return ;
	}
	
	$u.attr("disabled","disabled");
	$p.attr("disabled","disabled");
	
	var lt = $("#lt").val();
	
	$("#ul").val(u.length);
	$("#pl").val(p.length);
	$("#rsa").val(strEnc(u+p+lt , '1' , '2' , '3'));
	$("#loginForm")[0].submit();
}

function getImageCode(){
	if($('#div_image_code').length>0){
		$(".ajax-fc-container").captcha(); 
	}
}
