function checkform() {
  var start = document.forms['check']['start'].value;
  var end = document.forms['check']['end'].value;
  var date = document.forms['check']['date'].value;
  var st_list = document.getElementById("start_st").options; // start와 end의 list는 같음
  var start_match = false;
  var end_match = false;

  for (var i = 0; i<st_list.length; i++) {
    const data = st_list[i];

    if (data.value == start) {
      start_match = true;
    }
    else if (data.value == end) {
      end_match = true;
    }

    if (start_match == true && end_match == true) {
      break;
    }
  }

  if (!start_match || !end_match || date=="") {
    alert("올바른 값을 입력해주세요!\n(참고: 데이터에 없는 역이 있을 수 있습니다.)");
    return false;
  }
}