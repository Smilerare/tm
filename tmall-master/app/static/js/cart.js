var deleteOrderItem = false;
var deleteOrderItemid = 0;
$(function(){

	$("a.deleteOrderItem").click(function(){
		deleteOrderItem = false;
		var oiid = $(this).attr("oiid")
		deleteOrderItemid = oiid;
		$("#deleteConfirmModal").modal('show');
	});
	$("button.deleteConfirmButton").click(function(){
		deleteOrderItem = true;
		$("#deleteConfirmModal").modal('hide');
	});

	$('#deleteConfirmModal').on('hidden.bs.modal', function (e) {
		if(deleteOrderItem){
			var page="/foredeleteOrderItem/";
			$.post(
				    page,
				    {"oiid":deleteOrderItemid},
					function(data){
						if("success"==data.status){
							$("tr.cartProductItemTR[oiid="+deleteOrderItemid+"]").hide();
						}
						//else{
						//	location.href="login";
						//}
					}
				);

		}
	})

	$("img.cartProductItemIfSelected").click(function(){
		var selectit = $(this).attr("selectit")
		if("selectit"==selectit){
			$(this).attr("src","/static/img/site/cartNotSelected.png");
			$(this).attr("selectit","false")
			$(this).parents("tr.cartProductItemTR").css("background-color","#fff");

			var cid=$(this).attr("oiid");
			$.post("/changecart1/",{"cid":cid})
		}
		else{
			$(this).attr("src","/static/img/site/cartSelected.png");
			$(this).attr("selectit","selectit")
			$(this).parents("tr.cartProductItemTR").css("background-color","#FFF8E1");

			var cid=$(this).attr("oiid");
			$.post("/changecart/",{"cid":cid})
		}
		syncSelect();
		syncCreateOrderButton();
		calcCartSumPriceAndNumber();
	});
	$("img.selectAllItem").click(function(){
		var selectit = $(this).attr("selectit")
		if("selectit"==selectit){
			$("img.selectAllItem").attr("src","/static/img/site/cartNotSelected.png");
			$("img.selectAllItem").attr("selectit","false")
			$(".cartProductItemIfSelected").each(function(){
				$(this).attr("src","/static/img/site/cartNotSelected.png");
				$(this).attr("selectit","false");
				$(this).parents("tr.cartProductItemTR").css("background-color","#fff");

				var cid=$(this).attr("oiid");
				$.post("/changecart1/",{"cid":cid})
			});
		}
		else{
			$("img.selectAllItem").attr("src","/static/img/site/cartSelected.png");
			$("img.selectAllItem").attr("selectit","selectit")
			$(".cartProductItemIfSelected").each(function(){
				$(this).attr("src","/static/img/site/cartSelected.png");
				$(this).attr("selectit","selectit");
				$(this).parents("tr.cartProductItemTR").css("background-color","#FFF8E1");

				var cid=$(this).attr("oiid");
				$.post("/changecart/",{"cid":cid})
			});
		}
		syncCreateOrderButton();
		calcCartSumPriceAndNumber();


	});

	$(".orderItemNumberSetting").keyup(function(){
		var pid=$(this).attr("pid");
		var stock= $("span.orderItemStock[pid="+pid+"]").text();
		var price= $("span.orderItemPromotePrice[pid="+pid+"]").text();

		var num= $(".orderItemNumberSetting[pid="+pid+"]").val();
		num = parseInt(num);
		if(isNaN(num))
			num= 1;
		if(num<=0)
			num = 1;
		if(num>stock)
			num = stock;

		syncPrice(pid,num,price);
	});

	$(".numberPlus").click(function(){

		var pid=$(this).attr("pid");
		var stock= $("span.orderItemStock[pid="+pid+"]").text();
		var price= $("span.orderItemPromotePrice[pid="+pid+"]").text();
		var num= $(".orderItemNumberSetting[pid="+pid+"]").val();

		num++;
		if(num>stock)
			num = stock;
		syncPrice(pid,num,price);
	});
	$(".numberMinus").click(function(){
		var pid=$(this).attr("pid");
		var stock= $("span.orderItemStock[pid="+pid+"]").text();
		var price= $("span.orderItemPromotePrice[pid="+pid+"]").text();

		var num= $(".orderItemNumberSetting[pid="+pid+"]").val();
		--num;
		if(num<=0)
			num=1;
		syncPrice(pid,num,price);
	});

//	$("button.createOrderButton").click(function(){
//		var params = "";
//		$(".cartProductItemIfSelected").each(function(){
//			if("selectit"==$(this).attr("selectit")){
//				var oiid = $(this).attr("oiid");
//				params += "&oiid="+oiid;
//			}
//		});
//		params = params.substring(1);
//		location.href="forebuy?"+params;
//	});
	$("button.createOrderButton").click(function(){
		var f = confirm("确认支付？");
		if (f){
			$.post("/saveorder/",function(data){
				if (data.status = "success"){
					alert("支付成功")
					location.href="http://127.0.0.1:8000/order"
				}
			})
		}
	});

	//var ischoses = document.getElementsByClassName("cartProductItemIfSelected")
	//for (var i=0;i<ischoses.length;i++){
	//	ischose = ischoses[i]
	//	ischose.addEventListener("click",function(){
	//		cid = this.getAttribute("oiid")
	//		$.post("changecart/",{"cid":cid},function(data){
	//			if(data.status == "success"){
	//				window.location.href = "http://127.0.0.1:8000/cart/"
	//			}
	//		})
	//	})
	//}


})

function syncCreateOrderButton(){
	var selectAny = false;
	$(".cartProductItemIfSelected").each(function(){
		if("selectit"==$(this).attr("selectit")){
			selectAny = true;
		}
	});

	if(selectAny){
		$("button.createOrderButton").css("background-color","#C40000");
		$("button.createOrderButton").removeAttr("disabled");
	}
	else{
		$("button.createOrderButton").css("background-color","#AAAAAA");
		$("button.createOrderButton").attr("disabled","disabled");
	}

}
function syncSelect(){
	var selectAll = true;
	$(".cartProductItemIfSelected").each(function(){
		if("false"==$(this).attr("selectit")){
			selectAll = false;
		}
	});

	if(selectAll)
		$("img.selectAllItem").attr("src","/static/img/site/cartSelected.png");
		//cid = this.getAttribute("oiid")
		//	$.post("/changecart/",{"cid":cid},function(data){
		//		if(data.status == "success"){
		//			window.location.href = "http://127.0.0.1:8000/cart/"
		//		}
		//	})
	else
		$("img.selectAllItem").attr("src","/static/img/site/cartNotSelected.png");



}
function calcCartSumPriceAndNumber(){
	var sum = 0;
	var totalNumber = 0;
	$("img.cartProductItemIfSelected[selectit='selectit']").each(function(){
		var oiid = $(this).attr("oiid");
		var price =$(".cartProductItemSmallSumPrice[oiid="+oiid+"]").text();
		price = price.replace(/,/g, "");
		price = price.replace(/￥/g, "");
		sum += new Number(price);

		var num =$(".orderItemNumberSetting[oiid="+oiid+"]").val();
		totalNumber += new Number(num);

	});

	$("span.cartSumPrice").html("￥"+formatMoney(sum));
	$("span.cartTitlePrice").html("￥"+formatMoney(sum));
	$("span.cartSumNumber").html(totalNumber);
}
function syncPrice(pid,num,price){
	$(".orderItemNumberSetting[pid="+pid+"]").val(num);
	var cartProductItemSmallSumPrice = formatMoney(num*price);
	$(".cartProductItemSmallSumPrice[pid="+pid+"]").html("￥"+cartProductItemSmallSumPrice);
	calcCartSumPriceAndNumber();

	var page = "forechangeOrderItem";
	$.post(
		    page,
		    {"pid":pid,"number":num},
		    function(result){
				if("success"!=result){
					location.href="login";
				}
		    }
		);

}