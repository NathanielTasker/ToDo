//クリックイベント
$("#showoverlay").click(function() {
    //オーバーレイ用のボックスを作成
    $("body").append("<div id='overlay'></div>");
    //フェードエフェクト
    $("#overlay").fadeTo(500, 0.7);
    $("#edit_modal").fadeIn(500);
});
//閉じる際のクリックイベント
$("#close").click(function() {
    $("#edit_modal, #overlay").fadeOut(500, function() {
        $("#overlay").remove();
    });

});
$(window).resize(function() {
    //ボックスサイズ
    $("#edit_modal").css({
        top: ($(window).height() - $("#edit_modal").outerHeight()) / 2,
        left: ($(window).width() - $("#edit_modal").outerWidth()) / 2
    });
});
$(window).resize();​
