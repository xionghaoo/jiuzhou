var LANGX = 'gb', H = '75', ajaxDoing = false, query = {};
var _vCode, _fullName, _onlyfullName, _phone, _intrCode, _qq, _weixin, _birthday, _email, _fundPwd, _onlyfullPhone;
if (top.location.hostname != self.location.hostname) {
    location = '../../../';
}

function getYzm2() {
    $("#vImgreg").attr("src", "/v/vCode?m=reg&t=" + Math.random() + (new Date).getTime());
    $("#vImgreg").show();
}

function showYzm() {
    $(".identifyingCodePic1").show();
    $(".identifyingCodeRenovate1").css({'display': 'inline-block'});
    getYzm2();
}

function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return unescape(r[2]);
    }
    return null;
}

$(function () {
    var spreadCode = $.cookie("spreadCode", {path: "/"});
    if (spreadCode != null && spreadCode != '') {
        $("#intrCode").val(spreadCode).attr("readonly", "readonly");
    }
    $.getJSON("/data/json/limit/registerLimit.json?" + new Date().getTime(), {}, function (data) {
        allowRegister = (data.register && data.register > 0);
        needVcode = (data.vCode && data.vCode > 0);
        _vCode = data.vCode;
        _fullName = data.fullName;
        _onlyfullName = data.onlyfullName;
        _email = data.email;
        _phone = data.phone;
        _intrCode = data.intrCode;
        _qq = data.qq;
        _weixin = data.weixin;
        _birthday = data.birthday;
        _fundPwd = data.fundPwd;
        _onlyfullPhone = data.onlyfullPhone;
        if (needVcode) {
        } else {
            $("#vcodemoudlereg").hide();
        }
        if (_fullName == 0) {
        } else if (_fullName == 1) {
            $("#fullnameStar").append("*&nbsp;");
        } else {
            $("#fullname_moudle").hide();
        }
        if (_email == 1) {
            $("#emailStar").append("*&nbsp;");
        } else if (_email == 0) {
        } else {
            $("#email_moudle").hide();
        }
        if (_phone == 1) {
            $("#phoneStar").append("*&nbsp;");
        } else if (_phone == 0) {
        } else {
            $("#phone_moudle").hide();
        }
        if (_intrCode == 1) {
            $("#intrcodeStar").append("*&nbsp;");
        } else if (_intrCode == 0) {
        } else {
            $("#intrcodeMoudle").hide();
        }
        if (_qq == 1) {
            $("#qqStar").append("*&nbsp;");
        } else if (_qq == 0) {
        } else {
            $("#qq_moudle").hide();
        }
        if (_weixin == 1) {
            $("#weixinStar").append("*&nbsp;");
        } else if (_weixin == 0) {
        } else {
            $("#weixin_moudle").hide();
        }
        if (_birthday == 1) {
            $("#birthdayStar").append("*&nbsp;");
        } else if (_birthday == 0) {
        } else {
            $("#birthday_moudle").hide();
        }
        if (_fundPwd == 0) {
        } else if (_fundPwd == 1) {
            $("#pwdStar").append("*&nbsp;");
        } else {
            $("#pwd_moudle").hide();
        }
    }).error(function (XMLHttpRequest) {
    });
});

function checkusername() {
    var account = $("#account").val();
    var tel = /^[a-zA-Z0-9]{4,12}$/;
    if (account == '' || account == null) {
        layer.alert("????????????????????????", {icon: 2, shade: 0});
        return false;
    }
    if (!tel.test(account)) {
        layer.alert("????????????????????????????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function checkAccount() {
    $.ajax({
        url: "/v/user/checkUnique",
        type: "get",
        async: false,
        data: {type: 0, val: $("#account").val()},
        success: function (response) {
            if (response) {
                layer.alert("????????????????????????", {icon: 2, shade: 0});
                return false;
            }
            return true;
        }
    })
}

function checkpassword() {
    var password = $("#passwd").val();
    var tel = /[A-Za-z0-9]{6,11}/;
    if (password == '' || password == null) {
        layer.alert("?????????????????????", {icon: 2, shade: 0});
        return false;
    }
    if (!tel.test(password)) {
        layer.alert("?????????????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function checkfullname() {
    var fullName = $("#fullName").val();
    var Ch = /^[\u4e00-\u9fa5 ]{2,20}$/;
    if (fullName == '' || fullName == null) {
        layer.alert("???????????????????????????", {icon: 2, shade: 0});
        return false;
    }
    if (!Ch.test(fullName)) {
        layer.alert("???????????????????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function checkUnique() {
    var b = true;
    $.ajax({
        url: '/v/user/checkUnique',
        type: 'get',
        async: false,
        data: {val: $('#fullName').val(), type: 1},
        success: function (msg) {
            if (msg) {
                layer.alert("?????????????????????????????????????????????", {icon: 2, shade: 0});
                b = false;
            }
        }
    });
    return b;
}

function checkPhoneUnique() {
    var b = true;
    $.ajax({
        url: '/v/user/checkUnique',
        type: 'get',
        async: false,
        data: {val: $('#phone').val(), type: 2},
        success: function (msg) {
            if (msg) {
                layer.alert("?????????????????????????????????????????????", {icon: 2, shade: 0});
                b = false;
            }
        }
    });
    return b;
}

function checkpwd() {
    var pwd1 = $("#pwd1").val();
    var pwd2 = $("#pwd2").val();
    var pwd3 = $("#pwd3").val();
    var pwd4 = $("#pwd4").val();
    if (pwd1 == '' || pwd1 == null || pwd2 == '' || pwd2 == null || pwd3 == '' || pwd3 == null || pwd4 == '' || pwd4 == null) {
        layer.alert("???????????????????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function checkemail() {
    var email = $("#email").val();
    var tel = /([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})/;
    if (email == '' || email == null) {
        layer.alert("email???????????????", {icon: 2, shade: 0});
        return false;
    }
    if (!tel.test(email)) {
        layer.alert("email???????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function checkphone() {
    var phone = $("#phone").val();
    var tel = /^1\d{10}$/;
    if (phone == '' || phone == null) {
        layer.alert("???????????????????????????", {icon: 2, shade: 0});
        return false;
    }
    if (!tel.test(phone)) {
        layer.alert("?????????????????????????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function checkqq() {
    var qq = $("#qq").val();
    var tel = /^[1-9]\d{4,9}$/;
    if (qq == '' || qq == null) {
        layer.alert("QQ???????????????", {icon: 2, shade: 0});
        return false;
    }
    if (!tel.test(qq)) {
        layer.alert("QQ???????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function checkweixin() {
    var weixin = $("#weixin").val();
    var tel = /[a-z_\d-]+$/;
    if (weixin == '' || weixin == null) {
        layer.alert("?????????????????????", {icon: 2, shade: 0});
        return false;
    }
    if (!tel.test(weixin)) {
        layer.alert("?????????????????????", {icon: 2, shade: 0});
        return false;
    }
    return true;
}

function submitRegistr() {
    checkAccount();
    if (_intrCode == 1) {
        var intrCode = $("#intrCode").val();
        if (intrCode == '' || intrCode == null) {
            layer.alert("???????????????????????????", {icon: 2, shade: 0})
            return;
        }
    }
    if (!checkusername()) {
        return;
    }
    if (!checkpassword()) {
        return;
    }
    if ($("#confirmPassword").val() != $("#passwd").val()) {
        layer.alert("????????????????????????????????????????????????", {icon: 2, shade: 0});
        return;
    }
    if (_vCode > 0) {
        var vcode_val = $("#vCodeReg").val();
        if (vcode_val == '' || vcode_val == null) {
            layer.alert("??????????????????", {icon: 2, shade: 0});
            return;
        }
    }
    if (_fullName == 1) {
        if (!checkfullname()) {
            return;
        }
        if (_onlyfullName == 1) {
            if (!checkUnique()) {
                return;
            }
        }
    } else if (_fullName == 0) {
        var fullName = $("#fullName").val();
        if (fullName != null && fullName != '') {
            if (!checkfullname()) {
                return;
            }
        }
    }
    if (_birthday == 1) {
        var year = $("#year").val();
        var month = $("#month").val();
        var day = $("#day").val();
        if (year == '' || year == null || month == '' || month == null || day == '' || day == null) {
            layer.alert("?????????????????????", {icon: 2, shade: 0});
            return;
        }
    }
    if (_fundPwd == 1) {
        if (!checkpwd()) {
            return;
        }
    }
    if (_email == 1) {
        if (!checkemail()) {
            return;
        }
    } else if (_email == 0) {
        var email = $("#email").val();
        if (email != null && email != '') {
            if (!checkemail()) {
                return;
            }
        }
    }
    if (_phone == 1) {
        if (!checkphone()) {
            return false;
        }
        if (_onlyfullPhone == 1) {
            if (!checkPhoneUnique()) {
                return false;
            }
        }
    } else if (_phone == 0) {
        var phone = $("#phone").val();
        if (phone != null && phone != "") {
            if (!checkphone()) {
                return false;
            }
            if (_onlyfullPhone == 1) {
                if (!checkPhoneUnique()) {
                    return false;
                }
            }
        }
    }
    if (_qq == 1) {
        if (!checkqq()) {
            return false;
        }
    } else if (_qq == 0) {
        var qq = $("#qq").val();
        if (qq != null && qq != "") {
            if (!checkqq()) {
                return false;
            }
        }
    }
    if (_weixin == 1) {
        if (!checkweixin()) {
            return false;
        }
    } else if (_weixin == 0) {
        var weixin = $("#weixin").val();
        if (weixin != null && weixin != "") {
            if (!checkweixin()) {
                return false;
            }
        }
    }
    layer.confirm('?????????????????????????????????', {btn: ['??????', '????????????'], shade: 0}, function (index) {
        layer.close(index);
        var params = {};
        var myform = $('#myFORM').serializeArray();
        for (var i = 0; i < myform.length; i++) {
            if (myform[i].value) {
                params[myform[i].name] = myform[i].value;
            }
        }
        var md5Password = ($.cookie("md5Password", {path: "/"}) === 'true');
        params.password = md5Password ? hex_md5(params.password) : params.password;
        params.confirmPassword = md5Password ? hex_md5(params.confirmPassword) : params.confirmPassword;
        if (params.year && params.month && params.day) {
            params.birthday = params.year + "-" + params.month + "-" + params.day;
        }
        if (params.pwd1 && params.pwd2 && params.pwd3 && params.pwd4) {
            params.fundPwd = "" + params.pwd1 + params.pwd2 + params.pwd3 + params.pwd4;
        }
        $.ajax({
            url: '/v/user/reg', type: 'post', data: params, success: function (data) {
                layer.alert("???????????????????????????");
                $.cookie("account", $("#account").val(), {path: "/"});
                window.location.href = '/views/main.html';
            }, error: function () {
                $("#passwd").val("");
                $("#confirmPassword").val("");
            }
        });
    })
}