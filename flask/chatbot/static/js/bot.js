
//グローバル変数の宣言、代入
//変数のスコープがややこしくなるので、ここにはできるだけ処理を書かない

//今すぐ実行する処理

(function() {
    var botui = new BotUI('chatbot');
    // 初期メッセージ
    botui.message.add({
        content: 'こんにちは。chatbotです。'
    }).then(
        botui.message.add({
          delay:1000,
          content: '質問を入力してください。'
        }).then(function() {
            return botui.action.text({
                delay:1000,
                action: {
                    placeholder: '質問を入力...'
                }
            }).then(function(res) {
                //質問に対する回答を生成
                var answer;
                $.ajax("/question", {
                    type: "post",
                    data: {"question":res.value},  // 質問
                    dataType: "json",
                }).done(function(data) { // 通信成功
                    console.log("Ajax通信 成功");
                    information = JSON.parse(data.values).information
                    hit_question = JSON.parse(data.values).hit_question
                    hit_answer = JSON.parse(data.values).hit_answer
                    botui.message.add({
                        delay:1000,
                        type: "html",
                        content: `${information}<br>
                            質問：<br>
                            <b>${hit_question}</b><br>
                            回答：<br>
                            <b>${hit_answer}</b>
                            `
                    })
                }).fail(function(data) {
                    console.log("Ajax通信 失敗");// 通信失敗
                    return botui.message.add({
                        delay:1000,
                        type: "html",
                        content: `<b>すみません。通信に失敗しました。</b>`
                    })
                }).always(function(){
                    askEnd()//質問を終了するかどうか確認
                })
            })
        })
    );
}());



//DOMツリーが出来上がったら実行※画像読み込み前
document.addEventListener('DOMContentLoaded', function() {

});



//最後に実行※画像読み込み後
window.onload = function() {

};