function createOdds(odds, model) {
    var oldOddsArry = [];
    if (odds.indexOf(',') !== -1) {
        oldOddsArry = odds.split(',')
    } else {
        oldOddsArry.push(odds)
    }
    var newOdds = '';
    for (var i = 0; i < oldOddsArry.length; i++) {
        if (model === 1) {
            newOdds += (parseFloat(oldOddsArry[i]) / 10).oddFixed(4);
            newOdds += ','
        } else if (model === 2) {
            newOdds += (parseFloat(oldOddsArry[i]) / 100).oddFixed(4);
            newOdds += ','
        } else if (model === 0) {
            newOdds += (parseFloat(oldOddsArry[i])).oddFixed(4);
            newOdds += ','
        }
    }
    return newOdds.slice(0, newOdds.length - 1)
}

function getModel(money) {
    let model = 0;
    money = parseFloat(money);
    if (money.toString().indexOf(".") !== -1) {
        model = money.toString().split(".")[1].length;
    }
    return model
}


function getBetOdds(money, dataOdds) {
    let model = getModel(money)
    var betMultiple;
    var betMoney;
    var betOdds;
    var odds = dataOdds;
    if (model === 1) {
        betMultiple = (money * 10).oddFixed(0);
        betMoney = 0.1;
        betOdds = createOdds(odds,1);
    } else if (model === 2) {
        betMultiple = (money * 100).oddFixed(0);
        betMoney = 0.01;
        betOdds = createOdds(odds,2);
    } else if (model === 0) {
        betMultiple = money.oddFixed(0);
        betMoney = 1;
        betOdds = createOdds(odds,0);
    } else {
        // layer.alert('下注金额错误,只支持元角分模式', {icon: 2});
        // cancel();
        // isBeting = false;
        return
    }
    return {
        'odds': betOdds,
        "money": betMoney,
        "betModel": model,
        "multiple": betMultiple,
        // "totalMoney": (betMultiple * betMoney).oddFixed(2),
    };
}

Number.prototype.oddFixed = function (len) {
    var strValue = this + ''
    var start = strValue.indexOf('.')
    if (start > 0 && strValue.length > start + len + 1) {
        var endValue = parseInt(strValue.substr(start + len + 1, 1))
        if (endValue >= 5) {
            var temp = Math.pow(10, len + 1);
            strValue = (this + 1 / temp).toFixed(len);
        } else {
            strValue = strValue.substr(0, start + len + 1)
        }
        if (strValue && strValue.indexOf('.') === strValue.length - 1) {
            strValue = strValue.substr(0, strValue.length - 1)
        }
    }
    strValue = parseFloat(strValue) + '';
    return strValue
}
