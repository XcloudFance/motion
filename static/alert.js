var __alert_3 = document.createElement('div');
__alert_3.style = "position: fixed;left: 0;top: 0;width: 100%;height: 100%;background: rgba(0,0,0,0.25);border-radius:4px";
__alert_3.id = "alert_js";
document.getElementsByTagName("body")[0].appendChild(__alert_3);
__alert_3 = null;

var __alert_4 = document.createElement('div');
__alert_4.style = "width: 300px;height: 96px;background: #f5f5f5;margin: 0 auto;top: calc(100%/2 - 48px);position: absolute;left: calc(100%/2 - 150px);text-align:center;"
__alert_4.id = "alert_js_1"
document.getElementById('alert_js').appendChild(__alert_4);

var __alert_4_1 = document.createElement('p');
__alert_4_1.style = "margin-top:8px;border-radius:2px";
__alert_4_1.innerText = "发生了错误 请重试"
document.getElementById('alert_js_1').appendChild(__alert_4_1);

var __alert_5 = document.createElement('div');
__alert_5.style = "width: 100px;height: 24px;background-color: #ddd;margin: 0 auto;position: absolute;right: 5%;bottom: 7%;border-radius:2px;cursor: pointer;"
__alert_5.innerText = "好"
document.getElementById('alert_js_1').appendChild(__alert_5);

var alert_a = {
	log:function(msg){
		
	}
}