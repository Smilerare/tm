var deleteOrder = false;
var deleteOrderid = 0;

$(function(){
	$("a[orderStatus]").click(function(){
		var orderStatus = $(this).attr("orderStatus");
		if('all'==orderStatus){
			$("table[orderStatus]").show();
		}
		else{
			$("table[orderStatus]").hide();
			$("table[orderStatus="+orderStatus+"]").show();
		}
		$("div.orderType div").removeClass("selectedOrderType");
		$(this).parent("div").addClass("selectedOrderType");
	});

	$("a.deleteOrderLink").click(function(){
		deleteOrderid = $(this).attr("oid");
		deleteOrder = false;
		$("#deleteConfirmModal").modal("show");
	});

	$("button.deleteConfirmButton").click(function(){
		deleteOrder = true;
		$("#deleteConfirmModal").modal('hide');
	});
	//删除订单
	$('#deleteConfirmModal').on('hidden.bs.modal', function (e) {
		if(deleteOrder){
			var page="/foredeleteOrder/";
			$.post(
				    page,
				    {"oid":deleteOrderid},
				    function(data){
						if("success"==data.status){
							//隐藏订单，未删除
							$("table.orderListItemTable[oid="+deleteOrderid+"]").hide();
						}
						//else{
						//	location.href="login";
						//}
				    }
				);

		}
	})

	$(".ask2delivery").click(function(){
		var link = $(this).attr("link");
		$(this).hide();
		page = link;
		$.ajax({
			   url: page,
			   success: function(result){
				alert("卖家已收到，请耐心等待")
			   }
			});

	});
});
