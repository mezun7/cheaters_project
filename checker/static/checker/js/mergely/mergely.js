/**
 * Copyright (c) 2016 by Jamie Peabody, http://www.mergely.com
 * All rights reserved.
 * Version: 3.4.0 2016-02-07
 */
"use strict";
!function(a, b, c, d) {
    var e = {};
    e.Timer = function() {
        var a = this;
        a.start = function() {
            a.t0 = (new Date).getTime()
        },
        a.stop = function() {
            var b = (new Date).getTime(),
                c = b - a.t0;
            return a.t0 = b, c
        },
        a.start()
    },
    e.ChangeExpression = new RegExp(/(^(?![><\-])*\d+(?:,\d+)?)([acd])(\d+(?:,\d+)?)/),
    e.DiffParser = function(a) {
        for (var b = [], c = 0, d = a.split(/\n/), f = 0; f < d.length; ++f)
            if (0 != d[f].length) {
                var g = {},
                    h = e.ChangeExpression.exec(d[f]);
                if (null != h) {
                    var i = h[1].split(",");
                    g["lhs-line-from"] = i[0] - 1,
                    1 == i.length ? g["lhs-line-to"] = i[0] - 1 : g["lhs-line-to"] = i[1] - 1;
                    var j = h[3].split(",");
                    g["rhs-line-from"] = j[0] - 1,
                    1 == j.length ? g["rhs-line-to"] = j[0] - 1 : g["rhs-line-to"] = j[1] - 1,
                    g.op = h[2],
                    b[c++] = g
                }
            }
        return b
    },
    e.sizeOf = function(a) {
        var c,
            b = 0;
        for (c in a)
            a.hasOwnProperty(c) && b++;
        return b
    },
    e.LCS = function(a, b) {
        this.x = a.replace(/[ ]{1}/g, "\n"),
        this.y = b.replace(/[ ]{1}/g, "\n")
    },
    c.extend(e.LCS.prototype, {
        clear: function() {
            this.ready = 0
        },
        diff: function(a, b) {
            for (var c = new e.diff(this.x, this.y, {
                    ignorews: !1
                }), d = e.DiffParser(c.normal_form()), f = 0, g = 0, h = 0; h < d.length; ++h) {
                var i = d[h];
                if ("a" != i.op) {
                    f = c.getLines("lhs").slice(0, i["lhs-line-from"]).join(" ").length,
                    g = i["lhs-line-to"] + 1;
                    var j = c.getLines("lhs").slice(i["lhs-line-from"], g).join(" ");
                    "d" == i.op ? j += " " : f > 0 && "c" == i.op && (f += 1),
                    b(f, f + j.length)
                }
                if ("d" != i.op) {
                    f = c.getLines("rhs").slice(0, i["rhs-line-from"]).join(" ").length,
                    g = i["rhs-line-to"] + 1;
                    var k = c.getLines("rhs").slice(i["rhs-line-from"], g).join(" ");
                    "a" == i.op ? k += " " : f > 0 && "c" == i.op && (f += 1),
                    a(f, f + k.length)
                }
            }
        }
    }),
    e.CodeifyText = function(a) {
        this._max_code = 0,
        this._diff_codes = {},
        this.ctxs = {},
        this.options = {
            ignorews: !1
        },
        c.extend(this, a),
        this.lhs = a.lhs.split("\n"),
        this.rhs = a.rhs.split("\n")
    },
    c.extend(e.CodeifyText.prototype, {
        getCodes: function(a) {
            if (!this.ctxs.hasOwnProperty(a)) {
                var b = this._diff_ctx(this[a]);
                this.ctxs[a] = b,
                b.codes.length = Object.keys(b.codes).length
            }
            return this.ctxs[a].codes
        },
        getLines: function(a) {
            return this.ctxs[a].lines
        },
        _diff_ctx: function(a) {
            var b = {
                i: 0,
                codes: {},
                lines: a
            };
            return this._codeify(a, b), b
        },
        _codeify: function(a, b) {
            for (var d = (this._max_code, 0); d < a.length; ++d) {
                var e = a[d];
                this.options.ignorews && (e = e.replace(/\s+/g, ""));
                var f = this._diff_codes[e];
                void 0 != f ? b.codes[d] = f : (this._max_code++, this._diff_codes[e] = this._max_code, b.codes[d] = this._max_code)
            }
        }
    }),
    e.diff = function(a, b, d) {
        var f = c.extend({
            ignorews: !1
        }, d);
        this.codeify = new e.CodeifyText({
            lhs: a,
            rhs: b,
            options: f
        });
        var g = {
                codes: this.codeify.getCodes("lhs"),
                modified: {}
            },
            h = {
                codes: this.codeify.getCodes("rhs"),
                modified: {}
            },
            j = (g.codes.length + h.codes.length + 1, []),
            k = [];
        this._lcs(g, 0, g.codes.length, h, 0, h.codes.length, k, j),
        this._optimize(g),
        this._optimize(h),
        this.items = this._create_diffs(g, h)
    },
    c.extend(e.diff.prototype, {
        changes: function() {
            return this.items
        },
        getLines: function(a) {
            return this.codeify.getLines(a)
        },
        normal_form: function() {
            for (var a = "", b = 0; b < this.items.length; ++b) {
                var c = this.items[b],
                    d = "",
                    e = "",
                    f = "c";
                0 == c.lhs_deleted_count && c.rhs_inserted_count > 0 ? f = "a" : c.lhs_deleted_count > 0 && 0 == c.rhs_inserted_count && (f = "d"),
                d = 1 == c.lhs_deleted_count ? c.lhs_start + 1 : 0 == c.lhs_deleted_count ? c.lhs_start : c.lhs_start + 1 + "," + (c.lhs_start + c.lhs_deleted_count),
                e = 1 == c.rhs_inserted_count ? c.rhs_start + 1 : 0 == c.rhs_inserted_count ? c.rhs_start : c.rhs_start + 1 + "," + (c.rhs_start + c.rhs_inserted_count),
                a += d + f + e + "\n";
                var g = this.getLines("lhs"),
                    h = this.getLines("rhs");
                if (h && g) {
                    var i;
                    for (i = c.lhs_start; i < c.lhs_start + c.lhs_deleted_count; ++i)
                        a += "< " + g[i] + "\n";
                    for (c.rhs_inserted_count && c.lhs_deleted_count && (a += "---\n"), i = c.rhs_start; i < c.rhs_start + c.rhs_inserted_count; ++i)
                        a += "> " + h[i] + "\n"
                }
            }
            return a
        },
        _lcs: function(a, b, c, d, e, f, g, h) {
            for (; c > b && f > e && a.codes[b] == d.codes[e];)
                ++b,
                ++e;
            for (; c > b && f > e && a.codes[c - 1] == d.codes[f - 1];)
                --c,
                --f;
            if (b == c)
                for (; f > e;)
                    d.modified[e++] = !0;
            else if (e == f)
                for (; c > b;)
                    a.modified[b++] = !0;
            else {
                var i = this._sms(a, b, c, d, e, f, g, h);
                this._lcs(a, b, i.x, d, e, i.y, g, h),
                this._lcs(a, i.x, c, d, i.y, f, g, h)
            }
        },
        _sms: function(a, b, c, d, e, f, g, h) {
            var i = a.codes.length + d.codes.length + 1,
                j = b - e,
                k = c - f,
                l = c - b - (f - e),
                m = 0 != (1 & l),
                n = i - j,
                o = i - k,
                p = (c - b + f - e) / 2 + 1;
            h[n + j + 1] = b,
            g[o + k - 1] = c;
            var r,
                s,
                t,
                u,
                q = {
                    x: 0,
                    y: 0
                };
            for (r = 0; p >= r; ++r) {
                for (s = j - r; j + r >= s; s += 2) {
                    for (s == j - r ? t = h[n + s + 1] : (t = h[n + s - 1] + 1, j + r > s && h[n + s + 1] >= t && (t = h[n + s + 1])), u = t - s; c > t && f > u && a.codes[t] == d.codes[u];)
                        t++,
                        u++;
                    if (h[n + s] = t, m && s > k - r && k + r > s && g[o + s] <= h[n + s])
                        return q.x = h[n + s], q.y = h[n + s] - s, q
                }
                for (s = k - r; k + r >= s; s += 2) {
                    for (s == k + r ? t = g[o + s - 1] : (t = g[o + s + 1] - 1, s > k - r && g[o + s - 1] < t && (t = g[o + s - 1])), u = t - s; t > b && u > e && a.codes[t - 1] == d.codes[u - 1];)
                        t--,
                        u--;
                    if (g[o + s] = t, !m && s >= j - r && j + r >= s && g[o + s] <= h[n + s])
                        return q.x = h[n + s], q.y = h[n + s] - s, q
                }
            }
            throw "the algorithm should never come here."
        },
        _optimize: function(a) {
            for (var b = 0, c = 0; b < a.length;) {
                for (; b < a.length && (void 0 == a.modified[b] || 0 == a.modified[b]);)
                    b++;
                for (c = b; c < a.length && 1 == a.modified[c];)
                    c++;
                c < a.length && a.ctx[b] == a.codes[c] ? (a.modified[b] = !1, a.modified[c] = !0) : b = c
            }
        },
        _create_diffs: function(a, b) {
            for (var c = [], d = 0, e = 0, f = 0, g = 0; f < a.codes.length || g < b.codes.length;)
                if (f < a.codes.length && !a.modified[f] && g < b.codes.length && !b.modified[g])
                    f++,
                    g++;
                else {
                    for (d = f, e = g; f < a.codes.length && (g >= b.codes.length || a.modified[f]);)
                        f++;
                    for (; g < b.codes.length && (f >= a.codes.length || b.modified[g]);)
                        g++;
                    (f > d || g > e) && c.push({
                        lhs_start: d,
                        rhs_start: e,
                        lhs_deleted_count: f - d,
                        rhs_inserted_count: g - e
                    })
                }
            return c
        }
    }),
    e.mergely = function(a, b) {
        a && this.init(a, b)
    },
    c.extend(e.mergely.prototype, {
        name: "mergely",
        init: function(a, b) {
            this.diffView = new e.CodeMirrorDiffView(a, b),
            this.bind(a)
        },
        bind: function(a) {
            this.diffView.bind(a)
        }
    }),
    e.CodeMirrorDiffView = function(a, b) {
        d.defineExtension("centerOnCursor", function() {
            var a = this.cursorCoords(null, "local");
            this.scrollTo(null, (a.y + a.yBot) / 2 - this.getScrollerElement().clientHeight / 2)
        }),
        this.init(a, b)
    },
    c.extend(e.CodeMirrorDiffView.prototype, {
        init: function(a, b) {
            this.settings = {
                autoupdate: !0,
                autoresize: !0,
                rhs_margin: "right",
                wrap_lines: !1,
                line_numbers: !0,
                lcs: !0,
                sidebar: !0,
                viewport: !1,
                ignorews: !1,
                fadein: "fast",
                editor_width: "650px",
                editor_height: "400px",
                resize_timeout: 500,
                change_timeout: 150,
                fgcolor: {
                    a: "#4ba3fa",
                    c: "#a3a3a3",
                    d: "#ff7f7f",
                    ca: "#4b73ff",
                    cc: "#434343",
                    cd: "#ff4f4f"
                },
                bgcolor: "#eee",
                vpcolor: "rgba(0, 0, 200, 0.5)",
                lhs: function(a) {},
                rhs: function(a) {},
                loaded: function() {},
                _auto_width: function(a) {
                    return a
                },
                resize: function(b) {
                    var d = b ? 16 : 0,
                        e = c(a).parent().width() + d,
                        f = 0;
                    "auto" == this.width ? e = this._auto_width(e) : (e = this.width, this.editor_width = e),
                    "auto" == this.height ? f = c(a).parent().height() : (f = this.height, this.editor_height = f);
                    var g = e / 2 - 16 - 8,
                        h = f,
                        i = c(a);
                    i.find(".mergely-column").css({
                        width: g + "px"
                    }),
                    i.find(".mergely-column, .mergely-canvas, .mergely-margin, .mergely-column textarea, .CodeMirror-scroll, .cm-s-default").css({
                        height: h + "px"
                    }),
                    i.find(".mergely-canvas").css({
                        height: h + "px"
                    }),
                    i.find(".mergely-column textarea").css({
                        width: g + "px"
                    }),
                    i.css({
                        width: e,
                        height: f,
                        clear: "both"
                    }),
                    "none" == i.css("display") && (0 != this.fadein ? i.fadeIn(this.fadein) : i.show(), this.loaded && this.loaded()),
                    this.resized && this.resized()
                },
                _debug: "",
                resized: function() {}
            };
            var d = {
                mode: "text/plain",
                readOnly: !1,
                lineWrapping: this.settings.wrap_lines,
                lineNumbers: this.settings.line_numbers,
                gutters: ["merge", "CodeMirror-linenumbers"]
            };
            this.lhs_cmsettings = {},
            this.rhs_cmsettings = {},
            this.element = c(a),
            b && b.cmsettings && c.extend(this.lhs_cmsettings, d, b.cmsettings, b.lhs_cmsettings),
            b && b.cmsettings && c.extend(this.rhs_cmsettings, d, b.cmsettings, b.rhs_cmsettings),
            this.element.bind("destroyed", c.proxy(this.teardown, this)),
            c.data(a, "mergely", this),
            this._setOptions(b)
        },
        unbind: function() {
            null != this.changed_timeout && clearTimeout(this.changed_timeout),
            this.editor[this.id + "-lhs"].toTextArea(),
            this.editor[this.id + "-rhs"].toTextArea(),
            c(a).off(".mergely")
        },
        destroy: function() {
            this.element.unbind("destroyed", this.teardown),
            this.teardown()
        },
        teardown: function() {
            this.unbind()
        },
        lhs: function(a) {
            this.editor[this.id + "-lhs"].setValue(a)
        },
        rhs: function(a) {
            this.editor[this.id + "-rhs"].setValue(a)
        },
        update: function() {
            this._changing(this.id + "-lhs", this.id + "-rhs")
        },
        unmarkup: function() {
            this._clear()
        },
        scrollToDiff: function(a) {
            this.changes.length && ("next" == a ? this._current_diff = Math.min(++this._current_diff, this.changes.length - 1) : "prev" == a && (this._current_diff = Math.max(--this._current_diff, 0)), this._scroll_to_change(this.changes[this._current_diff]), this._changed(this.id + "-lhs", this.id + "-rhs"))
        },
        mergeCurrentChange: function(a) {
            this.changes.length && ("lhs" != a || this.lhs_cmsettings.readOnly ? "rhs" != a || this.rhs_cmsettings.readOnly || this._merge_change(this.changes[this._current_diff], "lhs", "rhs") : this._merge_change(this.changes[this._current_diff], "rhs", "lhs"))
        },
        scrollTo: function(a, b) {
            var c = this.editor[this.id + "-lhs"],
                d = this.editor[this.id + "-rhs"];
            "lhs" == a ? (c.setCursor(b), c.centerOnCursor()) : (d.setCursor(b), d.centerOnCursor())
        },
        _setOptions: function(a) {
            if (c.extend(this.settings, a), this.settings.hasOwnProperty("rhs_margin"))
                if ("left" == this.settings.rhs_margin)
                    this.element.find(".mergely-margin:last-child").insertAfter(this.element.find(".mergely-canvas"));
                else {
                    var b = this.element.find(".mergely-margin").last();
                    b.appendTo(b.parent())
                }
            this.settings.hasOwnProperty("sidebar") && (this.settings.sidebar ? this.element.find(".mergely-margin").css({
                display: "block"
            }) : this.element.find(".mergely-margin").css({
                display: "none"
            }));
            var d,
                e;
            this.settings.hasOwnProperty("wrap_lines") && this.editor && (d = this.editor[this.id + "-lhs"], e = this.editor[this.id + "-rhs"], d.setOption("lineWrapping", this.settings.wrap_lines), e.setOption("lineWrapping", this.settings.wrap_lines)),
            this.settings.hasOwnProperty("line_numbers") && this.editor && (d = this.editor[this.id + "-lhs"], e = this.editor[this.id + "-rhs"], d.setOption("lineNumbers", this.settings.line_numbers), e.setOption("lineNumbers", this.settings.line_numbers))
        },
        options: function(a) {
            return a ? (this._setOptions(a), this.settings.autoresize && this.resize(), this.settings.autoupdate && this.update(), void 0) : this.settings
        },
        swap: function() {
            if (!this.lhs_cmsettings.readOnly && !this.rhs_cmsettings.readOnly) {
                var a = this.editor[this.id + "-lhs"],
                    b = this.editor[this.id + "-rhs"],
                    c = b.getValue();
                b.setValue(a.getValue()),
                a.setValue(c)
            }
        },
        merge: function(a) {
            var b = this.editor[this.id + "-lhs"],
                c = this.editor[this.id + "-rhs"];
            "lhs" != a || this.lhs_cmsettings.readOnly ? this.rhs_cmsettings.readOnly || c.setValue(b.getValue()) : b.setValue(c.getValue())
        },
        get: function(a) {
            var b = this.editor[this.id + "-" + a],
                c = b.getValue();
            return void 0 == c ? "" : c
        },
        clear: function(a) {
            if (!("lhs" == a && this.lhs_cmsettings.readOnly || "rhs" == a && this.rhs_cmsettings.readOnly)) {
                var b = this.editor[this.id + "-" + a];
                b.setValue("")
            }
        },
        cm: function(a) {
            return this.editor[this.id + "-" + a]
        },
        search: function(a, b, c) {
            var f,
                d = this.editor[this.id + "-lhs"],
                e = this.editor[this.id + "-rhs"];
            f = "lhs" == a ? d : e,
            c = "prev" == c ? "findPrevious" : "findNext",
            (0 == f.getSelection().length || this.prev_query[a] != b) && (this.cursor[this.id] = f.getSearchCursor(b, {
                line: 0,
                ch: 0
            }, !1), this.prev_query[a] = b);
            var g = this.cursor[this.id];
            g[c]() ? f.setSelection(g.from(), g.to()) : g = f.getSearchCursor(b, {
                line: 0,
                ch: 0
            }, !1)
        },
        resize: function() {
            this.settings.resize(),
            this._changing(this.id + "-lhs", this.id + "-rhs"),
            this._set_top_offset(this.id + "-lhs")
        },
        diff: function() {
            var a = this.editor[this.id + "-lhs"].getValue(),
                b = this.editor[this.id + "-rhs"].getValue(),
                c = new e.diff(a, b, this.settings);
            return c.normal_form()
        },
        bind: function(b) {
            this.element.hide(),
            this.id = c(b).attr("id"),
            this.changed_timeout = null,
            this.chfns = {},
            this.chfns[this.id + "-lhs"] = [],
            this.chfns[this.id + "-rhs"] = [],
            this.prev_query = [],
            this.cursor = [],
            this._skipscroll = {},
            this.change_exp = new RegExp(/(\d+(?:,\d+)?)([acd])(\d+(?:,\d+)?)/);
            var e,
                f;
            if (void 0 != c.button)
                e = '<button title="Merge left"></button>',
                f = '<button title="Merge right"></button>';
            else {
                var g = "opacity:0.4;width:10px;height:15px;background-color:#888;cursor:pointer;text-align:center;color:#eee;border:1px solid: #222;margin-right:5px;margin-top: -2px;";
                e = '<div style="' + g + '" title="Merge left">&lt;</div>',
                f = '<div style="' + g + '" title="Merge right">&gt;</div>'
            }
            this.merge_rhs_button = c(f),
            this.merge_lhs_button = c(e);
            var h = this.settings.editor_height,
                i = this.settings.editor_width;
            this.element.append(c('<div class="mergely-margin" style="height: ' + h + '"><canvas id="' + this.id + '-lhs-margin" width="8px" height="' + h + '"></canvas></div>')),
            this.element.append(c('<div style="position:relative;width:' + i + "; height:" + h + '" id="' + this.id + '-editor-lhs" class="mergely-column"><textarea style="" id="' + this.id + '-lhs"></textarea></div>')),
            this.element.append(c('<div class="mergely-canvas" style="height: ' + h + '"><canvas id="' + this.id + "-lhs-" + this.id + '-rhs-canvas" style="width:28px" width="28px" height="' + h + '"></canvas></div>'));
            var j = c('<div class="mergely-margin" style="height: ' + h + '"><canvas id="' + this.id + '-rhs-margin" width="8px" height="' + h + '"></canvas></div>');
            this.settings.sidebar || this.element.find(".mergely-margin").css({
                display: "none"
            }),
            "left" == this.settings.rhs_margin && this.element.append(j),
            this.element.append(c('<div style="width:' + i + "; height:" + h + '" id="' + this.id + '-editor-rhs" class="mergely-column"><textarea style="" id="' + this.id + '-rhs"></textarea></div>')),
            "left" != this.settings.rhs_margin && this.element.append(j);
            var k = "#" + this.id + " .CodeMirror-gutter-text { padding: 5px 0 0 0; }#" + this.id + " .CodeMirror-lines pre, #" + this.id + " .CodeMirror-gutter-text pre { line-height: 18px; }.CodeMirror-linewidget { overflow: hidden; };";
            this.settings.autoresize && (k += this.id + " .CodeMirror-scroll { height: 100%; overflow: auto; }"),
            k += "\n.CodeMirror { line-height: 18px; }",
            c('<style type="text/css">' + k + "</style>").appendTo("head");
            var l = this.element.find("#" + this.id + "-rhs").get(0);
            if (!l)
                return void console.error("rhs textarea not defined - Mergely not initialized properly");
            var m = this.element.find("#" + this.id + "-lhs").get(0);
            if (!l)
                return void console.error("lhs textarea not defined - Mergely not initialized properly");
            var n = this;
            if (this.editor = [], this.editor[this.id + "-lhs"] = d.fromTextArea(m, this.lhs_cmsettings), this.editor[this.id + "-rhs"] = d.fromTextArea(l, this.rhs_cmsettings), this.editor[this.id + "-lhs"].on("change", function() {
                n.settings.autoupdate && n._changing(n.id + "-lhs", n.id + "-rhs")
            }), this.editor[this.id + "-lhs"].on("scroll", function() {
                n._scrolling(n.id + "-lhs")
            }), this.editor[this.id + "-rhs"].on("change", function() {
                n.settings.autoupdate && n._changing(n.id + "-lhs", n.id + "-rhs")
            }), this.editor[this.id + "-rhs"].on("scroll", function() {
                n._scrolling(n.id + "-rhs")
            }), this.settings.autoresize) {
                var o = null,
                    p = function(a) {
                        n.settings.resize && n.settings.resize(a),
                        n.editor[n.id + "-lhs"].refresh(),
                        n.editor[n.id + "-rhs"].refresh(),
                        n.settings.autoupdate && n._changing(n.id + "-lhs", n.id + "-rhs")
                    };
                c(a).on("resize.mergely", function() {
                    o && clearTimeout(o),
                    o = setTimeout(p, n.settings.resize_timeout)
                }),
                p(!0)
            }
            this.editor[this.id + "-lhs"].on("gutterClick", function(a, b) {
                return $(this.changes).filter(function(a, c) {
                    return b >= c["lhs-line-from"] && b <= c["lhs-line-to"] ? (this._current_diff = a, !0) : void 0
                }.bind(this))
            }.bind(this)),
            this.editor[this.id + "-rhs"].on("gutterClick", function(a, b) {
                $(this.changes).filter(function(a, c) {
                    return b >= c["rhs-line-from"] && b <= c["rhs-line-to"] ? (this._current_diff = a, !0) : void 0
                }.bind(this)),
                setTimeout(function() {
                    this.scrollToDiff()
                }.bind(this), 10)
            }.bind(this));
            var q;
            this.settings.lhs && (q = this.editor[this.id + "-lhs"].getDoc().setValue, this.settings.lhs(q.bind(this.editor[this.id + "-lhs"].getDoc()))),
            this.settings.rhs && (q = this.editor[this.id + "-rhs"].getDoc().setValue, this.settings.rhs(q.bind(this.editor[this.id + "-rhs"].getDoc())))
        },
        _scroll_to_change: function(a) {
            if (a) {
                var b = this,
                    c = b.editor[b.id + "-lhs"],
                    d = b.editor[b.id + "-rhs"];
                c.setCursor(Math.max(a["lhs-line-from"], 0), 0),
                d.setCursor(Math.max(a["rhs-line-from"], 0), 0),
                c.scrollIntoView({
                    line: a["lhs-line-to"]
                })
            }
        },
        _scrolling: function(a) {
            if (this._skipscroll[a] === !0)
                return void (this._skipscroll[a] = !1);
            var b = c(this.editor[a].getScrollerElement());
            void 0 == this.midway && (this.midway = (b.height() / 2 + b.offset().top).toFixed(2));
            var d = this.editor[a].coordsChar({
                    left: 0,
                    top: this.midway
                }),
                f = b.scrollTop(),
                g = b.scrollLeft();
            this.trace("scroll", "side", a),
            this.trace("scroll", "midway", this.midway),
            this.trace("scroll", "midline", d),
            this.trace("scroll", "top_to", f),
            this.trace("scroll", "left_to", g);
            var h = this.id + "-lhs",
                i = this.id + "-rhs";
            for (var j in this.editor)
                if (this.editor.hasOwnProperty(j) && a != j) {
                    for (var k = a.replace(this.id + "-", ""), l = j.replace(this.id + "-", ""), m = 0, n = null, o = !1, p = 0; p < this.changes.length; ++p) {
                        var q = this.changes[p];
                        d.line >= q[k + "-line-from"] && (n = q, d.line >= n[k + "-line-to"] && (q.hasOwnProperty(k + "-y-start") && q.hasOwnProperty(k + "-y-end") && q.hasOwnProperty(l + "-y-start") && q.hasOwnProperty(l + "-y-end") ? m += q[k + "-y-end"] - q[k + "-y-start"] - (q[l + "-y-end"] - q[l + "-y-start"]) : o = !0))
                    }
                    var r = this.editor[j].getViewport(),
                        s = !0;
                    if (n && (this.trace("scroll", "last change before midline", n), d.line >= r.from && d <= r.to && (s = !1)), this.trace("scroll", "scroll", s), s || o ? (this.trace("scroll", "scrolling other side", f - m), this._skipscroll[j] = !0, this.editor[j].scrollTo(g, f - m)) : this.trace("scroll", "not scrolling other side"), this.settings.autoupdate) {
                        var t = new e.Timer;
                        this._calculate_offsets(h, i, this.changes),
                        this.trace("change", "offsets time", t.stop()),
                        this._markup_changes(h, i, this.changes),
                        this.trace("change", "markup time", t.stop()),
                        this._draw_diff(h, i, this.changes),
                        this.trace("change", "draw time", t.stop())
                    }
                    this.trace("scroll", "scrolled")
                }
        },
        _changing: function(a, b) {
            this.trace("change", "changing-timeout", this.changed_timeout);
            var c = this;
            null != this.changed_timeout && clearTimeout(this.changed_timeout),
            this.changed_timeout = setTimeout(function() {
                var d = new e.Timer;
                c._changed(a, b),
                c.trace("change", "total time", d.stop())
            }, this.settings.change_timeout)
        },
        _changed: function(a, b) {
            this._clear(),
            this._diff(a, b)
        },
        _clear: function() {
            var b,
                c,
                d,
                f,
                g,
                h,
                i,
                a = this,
                j = function() {
                    for (f = new e.Timer, g = 0, i = c.lineCount(); i > g; ++g)
                        c.removeLineClass(g, "background");
                    for (g = 0; g < d.length; ++g)
                        h = d[g],
                        h.lines.length && a.trace("change", "clear text", h.lines[0].text),
                        h.clear();
                    c.clearGutter("merge"),
                    a.trace("change", "clear time", f.stop())
                };
            for (b in this.editor)
                this.editor.hasOwnProperty(b) && (c = this.editor[b], d = a.chfns[b], c.operation(j));
            a.chfns[b] = [];
            var k = this._draw_info(this.id + "-lhs", this.id + "-rhs"),
                l = k.clhs.get(0).getContext("2d"),
                m = k.crhs.get(0).getContext("2d"),
                n = k.dcanvas.getContext("2d");
            l.beginPath(),
            l.fillStyle = this.settings.bgcolor,
            l.strokeStyle = "#888",
            l.fillRect(0, 0, 6.5, k.visible_page_height),
            l.strokeRect(0, 0, 6.5, k.visible_page_height),
            m.beginPath(),
            m.fillStyle = this.settings.bgcolor,
            m.strokeStyle = "#888",
            m.fillRect(0, 0, 6.5, k.visible_page_height),
            m.strokeRect(0, 0, 6.5, k.visible_page_height),
            n.beginPath(),
            n.fillStyle = "#fff",
            n.fillRect(0, 0, this.draw_mid_width, k.visible_page_height)
        },
        _diff: function(a, b) {
            var c = this.editor[a].getValue(),
                d = this.editor[b].getValue(),
                f = new e.Timer,
                g = new e.diff(c, d, this.settings);
            this.trace("change", "diff time", f.stop()),
            this.changes = e.DiffParser(g.normal_form()),
            this.trace("change", "parse time", f.stop()),
            void 0 === this._current_diff && this.changes.length && (this._current_diff = 0, this._scroll_to_change(this.changes[0])),
            this.trace("change", "scroll_to_change time", f.stop()),
            this._calculate_offsets(a, b, this.changes),
            this.trace("change", "offsets time", f.stop()),
            this._markup_changes(a, b, this.changes),
            this.trace("change", "markup time", f.stop()),
            this._draw_diff(a, b, this.changes),
            this.trace("change", "draw time", f.stop())
        },
        _parse_diff: function(a, b, c) {
            this.trace("diff", "diff results:\n", c);
            for (var d = [], e = 0, f = c.split(/\n/), g = 0; g < f.length; ++g)
                if (0 != f[g].length) {
                    var h = {},
                        i = this.change_exp.exec(f[g]);
                    if (null != i) {
                        var j = i[1].split(",");
                        h["lhs-line-from"] = j[0] - 1,
                        1 == j.length ? h["lhs-line-to"] = j[0] - 1 : h["lhs-line-to"] = j[1] - 1;
                        var k = i[3].split(",");
                        h["rhs-line-from"] = k[0] - 1,
                        1 == k.length ? h["rhs-line-to"] = k[0] - 1 : h["rhs-line-to"] = k[1] - 1,
                        h["lhs-line-from"] < 0 && (h["lhs-line-from"] = 0),
                        h["lhs-line-to"] < 0 && (h["lhs-line-to"] = 0),
                        h["rhs-line-from"] < 0 && (h["rhs-line-from"] = 0),
                        h["rhs-line-to"] < 0 && (h["rhs-line-to"] = 0),
                        h.op = i[2],
                        d[e++] = h,
                        this.trace("diff", "change", h)
                    }
                }
            return d
        },
        _get_viewport: function(a, b) {
            var c = this.editor[a].getViewport(),
                d = this.editor[b].getViewport();
            return {
                from: Math.min(c.from, d.from),
                to: Math.max(c.to, d.to)
            }
        },
        _is_change_in_view: function(a, b) {
            return this.settings.viewport && (b["lhs-line-from"] < a.from && b["lhs-line-to"] < a.to || b["lhs-line-from"] > a.from && b["lhs-line-to"] > a.to || b["rhs-line-from"] < a.from && b["rhs-line-to"] < a.to || b["rhs-line-from"] > a.from && b["rhs-line-to"] > a.to) ? !1 : !0
        },
        _set_top_offset: function(a) {
            var b = this.editor[a].getScrollInfo().top;
            this.editor[a].scrollTo(null, 0);
            var c = this.element.find(".CodeMirror-measure").first(),
                d = c.offset().top - 4;
            return d ? (this.editor[a].scrollTo(null, b), this.draw_top_offset = .5 - d, !0) : !1
        },
        _calculate_offsets: function(a, b, d) {
            if (null == this.em_height) {
                if (!this._set_top_offset(a))
                    return;
                this.em_height = this.editor[a].defaultTextHeight(),
                this.em_height || (console.warn("Failed to calculate offsets, using 18 by default"), this.em_height = 18),
                this.draw_lhs_min = .5;
                var e = c("#" + a + "-" + b + "-canvas");
                if (e.length || console.error("failed to find canvas", "#" + a + "-" + b + "-canvas"), !e.width())
                    return void console.error("canvas width is 0");
                this.draw_mid_width = c("#" + a + "-" + b + "-canvas").width(),
                this.draw_rhs_max = this.draw_mid_width - .5,
                this.draw_lhs_width = 5,
                this.draw_rhs_width = 5,
                this.trace("calc", "change offsets calculated", {
                    top_offset: this.draw_top_offset,
                    lhs_min: this.draw_lhs_min,
                    rhs_max: this.draw_rhs_max,
                    lhs_width: this.draw_lhs_width,
                    rhs_width: this.draw_rhs_width
                })
            }
            for (var f = this.editor[a].charCoords({
                    line: 0
                }), g = this.editor[b].charCoords({
                    line: 0
                }), h = this._get_viewport(a, b), i = 0; i < d.length; ++i) {
                var j = d[i];
                if (this.settings.sidebar || this._is_change_in_view(h, j)) {
                    var o,
                        p,
                        q,
                        r,
                        s,
                        t,
                        u,
                        v,
                        w,
                        x,
                        k = j["lhs-line-from"] >= 0 ? j["lhs-line-from"] : 0,
                        l = j["lhs-line-to"] >= 0 ? j["lhs-line-to"] : 0,
                        m = j["rhs-line-from"] >= 0 ? j["rhs-line-from"] : 0,
                        n = j["rhs-line-to"] >= 0 ? j["rhs-line-to"] : 0;
                    this.editor[a].getOption("lineWrapping") || this.editor[b].getOption("lineWrapping") ? (s = this.editor[a].cursorCoords({
                        line: k,
                        ch: 0
                    }, "page"), v = this.editor[a].getLineHandle(k), o = {
                        top: s.top,
                        bottom: s.top + v.height
                    }, t = this.editor[a].cursorCoords({
                        line: l,
                        ch: 0
                    }, "page"), u = this.editor[a].getLineHandle(l), p = {
                        top: t.top,
                        bottom: t.top + u.height
                    }, s = this.editor[b].cursorCoords({
                        line: m,
                        ch: 0
                    }, "page"), w = this.editor[b].getLineHandle(m), q = {
                        top: s.top,
                        bottom: s.top + w.height
                    }, t = this.editor[b].cursorCoords({
                        line: n,
                        ch: 0
                    }, "page"), x = this.editor[b].getLineHandle(n), r = {
                        top: t.top,
                        bottom: t.top + x.height
                    }) : (o = {
                        top: f.top + k * this.em_height,
                        bottom: f.bottom + k * this.em_height + 2
                    }, p = {
                        top: f.top + l * this.em_height,
                        bottom: f.bottom + l * this.em_height + 2
                    }, q = {
                        top: g.top + m * this.em_height,
                        bottom: g.bottom + m * this.em_height + 2
                    }, r = {
                        top: g.top + n * this.em_height,
                        bottom: g.bottom + n * this.em_height + 2
                    }),
                    "a" == j.op ? m > 0 && (o.top = o.bottom, o.bottom += this.em_height, p = o) : "d" == j.op && k > 0 && (q.top = q.bottom, q.bottom += this.em_height, r = q),
                    j["lhs-y-start"] = this.draw_top_offset + o.top,
                    "c" == j.op || "d" == j.op ? j["lhs-y-end"] = this.draw_top_offset + p.bottom : j["lhs-y-end"] = this.draw_top_offset + p.top,
                    j["rhs-y-start"] = this.draw_top_offset + q.top,
                    "c" == j.op || "a" == j.op ? j["rhs-y-end"] = this.draw_top_offset + r.bottom : j["rhs-y-end"] = this.draw_top_offset + r.top,
                    this.trace("calc", "change calculated", i, j)
                } else
                    delete j["lhs-y-start"],
                    delete j["lhs-y-end"],
                    delete j["rhs-y-start"],
                    delete j["rhs-y-end"]
            }
            return d
        },
        _markup_changes: function(a, b, d) {
            c(".merge-button").remove();
            var f = this,
                g = this.editor[a],
                h = this.editor[b],
                i = this._current_diff,
                j = new e.Timer;
            g.operation(function() {
                for (var a = 0; a < d.length; ++a) {
                    var b = d[a],
                        c = b["lhs-line-from"] >= 0 ? b["lhs-line-from"] : 0,
                        e = b["lhs-line-to"] >= 0 ? b["lhs-line-to"] : 0,
                        j = b["rhs-line-from"] >= 0 ? b["rhs-line-from"] : 0,
                        l = (b["rhs-line-to"] >= 0 ? b["rhs-line-to"] : 0, ["mergely", "lhs", b.op, "cid-" + a]);
                    if (g.addLineClass(c, "background", "start"), g.addLineClass(e, "background", "end"), i == a && (c != e && g.addLineClass(c, "background", "current"), g.addLineClass(e, "background", "current")), 0 == c && 0 == e && 0 == j)
                        g.addLineClass(c, "background", l.join(" ")),
                        g.addLineClass(c, "background", "first");
                    else
                        for (var m = c; e >= m; ++m)
                            g.addLineClass(m, "background", l.join(" ")),
                            g.addLineClass(m, "background", l.join(" "));
                    if (!h.getOption("readOnly")) {
                        var n = f.merge_rhs_button.clone();
                        n.button && n.button({
                            icons: {
                                primary: "ui-icon-triangle-1-e"
                            },
                            text: !1
                        }),
                        n.addClass("merge-button"),
                        n.attr("id", "merge-rhs-" + a),
                        g.setGutterMarker(c, "merge", n.get(0))
                    }
                }
            });
            var k = this._get_viewport(a, b);
            this.trace("change", "markup lhs-editor time", j.stop()),
            h.operation(function() {
                for (var a = 0; a < d.length; ++a) {
                    var b = d[a],
                        c = b["lhs-line-from"] >= 0 ? b["lhs-line-from"] : 0,
                        j = (b["lhs-line-to"] >= 0 ? b["lhs-line-to"] : 0, b["rhs-line-from"] >= 0 ? b["rhs-line-from"] : 0),
                        l = b["rhs-line-to"] >= 0 ? b["rhs-line-to"] : 0;
                    if (f._is_change_in_view(k, b)) {
                        var m = ["mergely", "rhs", b.op, "cid-" + a];
                        if (h.addLineClass(j, "background", "start"), h.addLineClass(l, "background", "end"), i == a && (j != l && h.addLineClass(j, "background", "current"), h.addLineClass(l, "background", "current")), 0 == j && 0 == l && 0 == c)
                            h.addLineClass(j, "background", m.join(" ")),
                            h.addLineClass(j, "background", "first");
                        else
                            for (var n = j; l >= n; ++n)
                                h.addLineClass(n, "background", m.join(" ")),
                                h.addLineClass(n, "background", m.join(" "));
                        if (!g.getOption("readOnly")) {
                            var o = f.merge_lhs_button.clone();
                            o.button && o.button({
                                icons: {
                                    primary: "ui-icon-triangle-1-w"
                                },
                                text: !1
                            }),
                            o.addClass("merge-button"),
                            o.attr("id", "merge-lhs-" + a),
                            h.setGutterMarker(j, "merge", o.get(0))
                        }
                    }
                }
            }),
            this.trace("change", "markup rhs-editor time", j.stop());
            var m,
                n,
                o,
                p,
                l = [];
            for (m = 0; this.settings.lcs && m < d.length; ++m) {
                var q = d[m],
                    r = q["lhs-line-from"] >= 0 ? q["lhs-line-from"] : 0,
                    s = q["lhs-line-to"] >= 0 ? q["lhs-line-to"] : 0,
                    t = q["rhs-line-from"] >= 0 ? q["rhs-line-from"] : 0,
                    u = q["rhs-line-to"] >= 0 ? q["rhs-line-to"] : 0;
                if (this._is_change_in_view(k, q))
                    if ("d" == q.op) {
                        var v = r,
                            w = s,
                            x = g.lineInfo(w);
                        x && l.push([g, {
                            line: v,
                            ch: 0
                        }, {
                            line: w,
                            ch: x.text.length
                        }, {
                            className: "mergely ch d lhs"
                        }])
                    } else if ("c" == q.op)
                        for (n = r, o = t, p = 0; n >= 0 && s >= n || o >= 0 && u >= o; ++n, ++o) {
                            var y,
                                z;
                            if (o + p > u)
                                y = g.getLine(n),
                                l.push([g, {
                                    line: n,
                                    ch: 0
                                }, {
                                    line: n,
                                    ch: y.length
                                }, {
                                    className: "mergely ch d lhs"
                                }]);
                            else if (n + p > s)
                                z = h.getLine(o),
                                l.push([h, {
                                    line: o,
                                    ch: 0
                                }, {
                                    line: o,
                                    ch: z.length
                                }, {
                                    className: "mergely ch a rhs"
                                }]);
                            else {
                                y = g.getLine(n),
                                z = h.getLine(o);
                                var A = new e.LCS(y, z);
                                A.diff(function(a, b) {
                                    l.push([h, {
                                        line: o,
                                        ch: a
                                    }, {
                                        line: o,
                                        ch: b
                                    }, {
                                        className: "mergely ch a rhs"
                                    }])
                                }, function(a, b) {
                                    l.push([g, {
                                        line: n,
                                        ch: a
                                    }, {
                                        line: n,
                                        ch: b
                                    }, {
                                        className: "mergely ch d lhs"
                                    }])
                                })
                            }
                        }
            }
            this.trace("change", "LCS marktext time", j.stop()),
            g.operation(function() {
                for (var a = 0; a < l.length; ++a) {
                    var b = l[a];
                    b[0].doc.id == g.getDoc().id && f.chfns[f.id + "-lhs"].push(b[0].markText(b[1], b[2], b[3]))
                }
            }),
            h.operation(function() {
                for (var a = 0; a < l.length; ++a) {
                    var b = l[a];
                    b[0].doc.id == h.getDoc().id && f.chfns[f.id + "-rhs"].push(b[0].markText(b[1], b[2], b[3]))
                }
            }),
            this.trace("change", "LCS markup time", j.stop());
            var B = {
                lhs: g,
                rhs: h
            };
            c(".merge-button").on("click", function(a) {
                var b = "rhs",
                    d = "lhs",
                    e = c(this).parents("#" + f.id + "-editor-lhs");
                e.length && (b = "lhs", d = "rhs");
                var g = B[b].coordsChar({
                        left: a.pageX,
                        top: a.pageY
                    }),
                    h = null,
                    i = B[b].lineInfo(g.line);
                c.each(i.bgClass.split(" "), function(a, b) {
                    return 0 == b.indexOf("cid-") ? (h = parseInt(b.split("-")[1], 10), !1) : void 0
                });
                var j = f.changes[h];
                return f._merge_change(j, b, d), !1
            });
            var C = $("#mergely-lhs ~ .CodeMirror").find(".CodeMirror-linenumber"),
                D = $("#mergely-rhs ~ .CodeMirror").find(".CodeMirror-linenumber");
            D.removeClass("mergely current"),
            C.removeClass("mergely current");
            for (var m = 0; m < d.length; ++m) {
                if (i == m && "d" !== q.op) {
                    var n,
                        q = d[m],
                        E = q["rhs-line-from"],
                        F = q["rhs-line-to"] + 1;
                    for (n = E; F > n; n++) {
                        var G = (n + 1).toString();
                        D.filter(function(a, b) {
                            return $(b).text() === G
                        }).addClass("mergely current")
                    }
                }
                if (i == m && "a" !== q.op) {
                    var q = d[m];
                    for (E = q["lhs-line-from"], F = q["lhs-line-to"] + 1, n = E; F > n; n++) {
                        var G = (n + 1).toString();
                        C.filter(function(a, b) {
                            return $(b).text() === G
                        }).addClass("mergely current")
                    }
                }
            }
            this.trace("change", "markup buttons time", j.stop())
        },
        _merge_change: function(a, b, c) {
            if (a) {
                var h,
                    i,
                    j,
                    e = this.editor[this.id + "-lhs"],
                    f = this.editor[this.id + "-rhs"],
                    g = {
                        lhs: e,
                        rhs: f
                    },
                    k = g[b].getRange(d.Pos(a[b + "-line-from"], 0), d.Pos(a[b + "-line-to"] + 1, 0));
                if ("c" == a.op)
                    g[c].replaceRange(k, d.Pos(a[c + "-line-from"], 0), d.Pos(a[c + "-line-to"] + 1, 0));
                else if ("rhs" == b)
                    if ("a" == a.op)
                        g[c].replaceRange(k, d.Pos(a[c + "-line-from"] + 1, 0), d.Pos(a[c + "-line-to"] + 1, 0));
                    else
                        for (i = parseInt(a[c + "-line-from"], 10), j = parseInt(a[c + "-line-to"], 10), h = j; h >= i; --h)
                            g[c].setCursor({
                                line: h,
                                ch: -1
                            }),
                            g[c].execCommand("deleteLine");
                else if ("lhs" == b)
                    if ("a" == a.op)
                        for (i = parseInt(a[c + "-line-from"], 10), j = parseInt(a[c + "-line-to"], 10), h = j; h >= i; --h)
                            g[c].setCursor({
                                line: h,
                                ch: -1
                            }),
                            g[c].execCommand("deleteLine");
                    else
                        g[c].replaceRange(k, d.Pos(a[c + "-line-from"] + 1, 0));
                g.lhs.setValue(g.lhs.getValue()),
                g.rhs.setValue(g.rhs.getValue()),
                this._scroll_to_change(a)
            }
        },
        _draw_info: function(a, d) {
            var e = c(this.editor[a].getScrollerElement()).height(),
                f = c(this.editor[a].getScrollerElement()).children(":first-child").height(),
                g = b.getElementById(a + "-" + d + "-canvas");
            if (void 0 == g)
                throw "Failed to find: " + a + "-" + d + "-canvas";
            var h = this.element.find("#" + this.id + "-lhs-margin"),
                i = this.element.find("#" + this.id + "-rhs-margin");
            return {
                visible_page_height: e,
                gutter_height: f,
                visible_page_ratio: e / f,
                margin_ratio: e / f,
                lhs_scroller: c(this.editor[a].getScrollerElement()),
                rhs_scroller: c(this.editor[d].getScrollerElement()),
                lhs_lines: this.editor[a].lineCount(),
                rhs_lines: this.editor[d].lineCount(),
                dcanvas: g,
                clhs: h,
                crhs: i,
                lhs_xyoffset: c(h).offset(),
                rhs_xyoffset: c(i).offset()
            }
        },
        _draw_diff: function(a, b, d) {
            var e = this._draw_info(a, b),
                f = e.clhs.get(0),
                g = e.crhs.get(0),
                h = e.dcanvas.getContext("2d"),
                i = f.getContext("2d"),
                j = g.getContext("2d");
            this.trace("draw", "visible_page_height", e.visible_page_height),
            this.trace("draw", "gutter_height", e.gutter_height),
            this.trace("draw", "visible_page_ratio", e.visible_page_ratio),
            this.trace("draw", "lhs-scroller-top", e.lhs_scroller.scrollTop()),
            this.trace("draw", "rhs-scroller-top", e.rhs_scroller.scrollTop()),
            c.each(this.element.find("canvas"), function() {
                c(this).get(0).height = e.visible_page_height
            }),
            e.clhs.unbind("click"),
            e.crhs.unbind("click"),
            i.beginPath(),
            i.fillStyle = this.settings.bgcolor,
            i.strokeStyle = "#888",
            i.fillRect(0, 0, 6.5, e.visible_page_height),
            i.strokeRect(0, 0, 6.5, e.visible_page_height),
            j.beginPath(),
            j.fillStyle = this.settings.bgcolor,
            j.strokeStyle = "#888",
            j.fillRect(0, 0, 6.5, e.visible_page_height),
            j.strokeRect(0, 0, 6.5, e.visible_page_height);
            for (var k = this._get_viewport(a, b), l = 0; l < d.length; ++l) {
                var m = d[l],
                    n = this.settings.fgcolor[m.op];
                this._current_diff == l && (n = "#000"),
                this.trace("draw", m);
                var o = (m["lhs-y-start"] + e.lhs_scroller.scrollTop()) * e.visible_page_ratio,
                    p = (m["lhs-y-end"] + e.lhs_scroller.scrollTop()) * e.visible_page_ratio + 1,
                    q = (m["rhs-y-start"] + e.rhs_scroller.scrollTop()) * e.visible_page_ratio,
                    r = (m["rhs-y-end"] + e.rhs_scroller.scrollTop()) * e.visible_page_ratio + 1;
                if (this.trace("draw", "marker calculated", o, p, q, r), i.beginPath(), i.fillStyle = n, i.strokeStyle = "#000", i.lineWidth = .5, i.fillRect(1.5, o, 4.5, Math.max(p - o, 5)), i.strokeRect(1.5, o, 4.5, Math.max(p - o, 5)), j.beginPath(), j.fillStyle = n, j.strokeStyle = "#000", j.lineWidth = .5, j.fillRect(1.5, q, 4.5, Math.max(r - q, 5)), j.strokeRect(1.5, q, 4.5, Math.max(r - q, 5)), this._is_change_in_view(k, m)) {
                    o = m["lhs-y-start"],
                    p = m["lhs-y-end"],
                    q = m["rhs-y-start"],
                    r = m["rhs-y-end"];
                    var s = 3;
                    h.beginPath(),
                    h.strokeStyle = n,
                    h.lineWidth = this._current_diff == l ? 1.5 : 1;
                    var t = this.draw_lhs_width,
                        u = p - o - 1,
                        v = this.draw_lhs_min,
                        w = o;
                    h.moveTo(v, w),
                    "Microsoft Internet Explorer" == navigator.appName ? (h.lineTo(this.draw_lhs_min + this.draw_lhs_width, o), h.lineTo(this.draw_lhs_min + this.draw_lhs_width, p + 1), h.lineTo(this.draw_lhs_min, p + 1)) : (0 >= u ? h.lineTo(v + t, w) : (h.arcTo(v + t, w, v + t, w + s, s), h.arcTo(v + t, w + u, v + t - s, w + u, s)), h.lineTo(v, w + u)),
                    h.stroke(),
                    t = this.draw_rhs_width,
                    u = r - q - 1,
                    v = this.draw_rhs_max,
                    w = q,
                    h.moveTo(v, w),
                    "Microsoft Internet Explorer" == navigator.appName ? (h.lineTo(this.draw_rhs_max - this.draw_rhs_width, q), h.lineTo(this.draw_rhs_max - this.draw_rhs_width, r + 1), h.lineTo(this.draw_rhs_max, r + 1)) : (0 >= u ? h.lineTo(v - t, w) : (h.arcTo(v - t, w, v - t, w + s, s), h.arcTo(v - t, w + u, v - s, w + u, s)), h.lineTo(v, w + u)),
                    h.stroke();
                    var x = this.draw_lhs_min + this.draw_lhs_width,
                        y = o + (p + 1 - o) / 2,
                        z = this.draw_rhs_max - this.draw_rhs_width,
                        A = q + (r + 1 - q) / 2;
                    h.moveTo(x, y),
                    y == A ? h.lineTo(z, A) : h.bezierCurveTo(x + 12, y - 3, z - 12, A - 3, z, A),
                    h.stroke()
                }
            }
            i.fillStyle = this.settings.vpcolor,
            j.fillStyle = this.settings.vpcolor;
            var B = e.clhs.height() * e.visible_page_ratio,
                C = e.lhs_scroller.scrollTop() / e.gutter_height * e.clhs.height(),
                D = e.crhs.height() * e.visible_page_ratio,
                E = e.rhs_scroller.scrollTop() / e.gutter_height * e.crhs.height();
            this.trace("draw", "cls.height", e.clhs.height()),
            this.trace("draw", "lhs_scroller.scrollTop()", e.lhs_scroller.scrollTop()),
            this.trace("draw", "gutter_height", e.gutter_height),
            this.trace("draw", "visible_page_ratio", e.visible_page_ratio),
            this.trace("draw", "lhs from", C, "lhs to", B),
            this.trace("draw", "rhs from", E, "rhs to", D),
            i.fillRect(1.5, C, 4.5, B),
            j.fillRect(1.5, E, 4.5, D),
            e.clhs.click(function(a) {
                var b = a.pageY - e.lhs_xyoffset.top - B / 2,
                    c = Math.max(0, b / f.height * e.lhs_scroller.get(0).scrollHeight);
                e.lhs_scroller.scrollTop(c)
            }),
            e.crhs.click(function(a) {
                var b = a.pageY - e.rhs_xyoffset.top - D / 2,
                    c = Math.max(0, b / g.height * e.rhs_scroller.get(0).scrollHeight);
                e.rhs_scroller.scrollTop(c)
            })
        },
        trace: function(a) {
            this.settings._debug.indexOf(a) >= 0 && (arguments[0] = a + ":", console.log([].slice.apply(arguments)))
        }
    }),
    c.pluginMaker = function(a) {
        c.fn[a.prototype.name] = function(b) {
            var f,
                d = c.makeArray(arguments),
                e = d.slice(1);
            return this.each(function() {
                var g = c.data(this, a.prototype.name);
                if (g) {
                    if ("string" == typeof b)
                        f = g[b].apply(g, e);
                    else if (g.update)
                        return g.update.apply(g, d)
                } else {
                    new a(this, b)
                }
            }), void 0 != f ? f : void 0
        }
    },
    c.pluginMaker(e.mergely)
}(window, document, jQuery, CodeMirror);
