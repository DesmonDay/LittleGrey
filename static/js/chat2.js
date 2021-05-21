// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").live("submit", function() {
        newMessage($(this));
        return false;
    });
    $("#messageform").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    
    $("#messageform2").live("submit", function() {
        newMessage2($(this));
        return false;
    });
    $("#messageform2").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage2($(this));
            return false;
        }
    });

    updater.poll();
    updater2.poll();
});

function newMessage(form) {
    var message = form.formToDict();
    var disabled = form.find("input[id=submit1]");
    disabled.disable();
    $.postJSON("/a/message/new", message, function(response) {
        updater.showMessage(response);
        if (message.id) {
            form.parent().remove();
        } else {
            form.find("input[id=message]").val("").select();
            disabled.enable();
        }
    });
}

function newMessage2(form) {
    var message = form.formToDict();
    var disabled = form.find("input[id=submit2]");
    disabled.disable();
    $.postJSON("/a/message/new2", message, function(response) {
        updater2.showMessage(response);
        if (message.id) {
            form.parent().remove();
        } else {
            form.find("input[id=message2]").val("").select();
            disabled.enable();
        }
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url, data: $.param(args), dataType: "text", type: "POST",
            success: function(response) {
        if (callback) callback(eval("(" + response + ")"));
    }, error: function(response) {
        console.log("ERROR:", response)
    }});
};

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

jQuery.fn.disable = function() {
    this.enable(false);
    return this;
};

jQuery.fn.enable = function(opt_enable) {
    if (arguments.length && !opt_enable) {
        this.attr("disabled", "disabled");
    } else {
        this.removeAttr("disabled");
    }
    return this;
};

var updater = {
    errorSleepTime: 500,
    cursor: null,

    poll: function() {
        var args = {"_xsrf": getCookie("_xsrf")};
        if (updater.cursor) args.cursor = updater.cursor;
        $.ajax({url: "/a/message/updates", type: "POST", dataType: "text",
                data: $.param(args), success: updater.onSuccess,
                error: updater.onError});
        //GET - 从指定的资源请求数据
        //POST - 向指定的资源提交要处理的数据
    },

    onSuccess: function(response) {
        try {
            updater.newMessages(eval("(" + response + ")"));
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 0);
    },

    onError: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },

    newMessages: function(response) {
        if (!response.messages) return;
        updater.cursor = response.cursor;
        var messages = response.messages;
        updater.cursor = messages[messages.length - 1].id;
        console.log(messages.length, "new messages, cursor:", updater.cursor);
        for (var i = 0; i < messages.length; i++) {
            updater.showMessage(messages[i]);
        }
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node1 = $(message.html);
        //node1.hide();
        $("#inbox").append(node1);
        //node1.slideDown();
        var node2 = $(message.html_kg);
        node2.hide();
        $("#inbox2").empty();
        $("#inbox2").append(node2);
        node2.show();
    }
};

var updater2 = {
    errorSleepTime: 500,
    cursor: null,
    
    pool: function() {
        var args = {"_xsrf": getCookie("_xsrf")};
        if (updater2.cursor) args.cursor = updater2.cursor;
        $.ajax({url: "/a/message/updates", type: "POST", dataType: "text",
                data: $.param(args), success: updater2.onSuccess,
                error: updater2.onError});
    },

    onSuccess: function(response) {
        try {
            updater2.newMessages(eval("(" + response + ")"));
        } catch (e) {
            updater2.onError();
            return;
        }
        updater2.errorSleepTime = 500;
        window.setTimeout(updater2.poll, 0);
    },

    onError: function(response) {
        updater2.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater2.errorSleepTime, "ms");
        window.setTimeout(updater2.poll, updater2.errorSleepTime);
    },
    
    newMessages: function(response) {
        if (!response.messages) return;
        updater2.cursor = response.cursor;
        var messages = response.messages;
        updater2.cursor = messages[messages.length - 1].id;
        console.log(messages.length, "new messages, cursor:", updater2.cursor);
        for (var i = 0; i < messages.length; i++) {
            updater2.showMessage(messages[i]);
        }
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node1 = $(message.html);
        //node1.hide();
        $("#inbox3").append(node1);
        //node1.slideDown();
        var node2 = $(message.html_kg);
        node2.hide();
        $("#inbox4").empty();
        $("#inbox4").append(node2);
        node2.show();
    }
};
