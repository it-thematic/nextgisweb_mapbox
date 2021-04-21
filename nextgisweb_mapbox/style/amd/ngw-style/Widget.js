/* globals define, console */
define([
    "dojo/_base/declare",
    "dojo/aspect",
    "dojo/json",
    "dojo/request/xhr",
    "dijit/layout/ContentPane",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "ngw/route",
    "ngw-pyramid/i18n!style",
    "ngw-pyramid/hbs-i18n",
    "ngw-resource/serialize",
    "dojo/text!./template/Widget.hbs",
    // template
    "dijit/Dialog",
    "dijit/layout/BorderContainer",
    "dijit/form/Textarea",
    "ngw-pyramid/form/CodeMirror",
    "dijit/Toolbar",
    "dojox/layout/TableContainer",
    "dijit/layout/TabContainer",
    "dijit/form/TextBox",
    "dijit/ColorPalette",
    "dijit/form/NumberSpinner"
], function (
    declare,
    aspect,
    json,
    xhr,
    ContentPane,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    route,
    i18n,
    hbsI18n,
    serialize,
    template
) {
    return declare([ContentPane, serialize.Mixin, _TemplatedMixin, _WidgetsInTemplateMixin], {
        templateString: hbsI18n(template, i18n),
        title: i18n.gettext("Mapbox style"),
        prefix: "mapbox_style",

        validateDataInMixin: function (errback) {
            // Добавить механизм валидации загруженного стиля
            return true;
        },

        serializeInMixin: function (data) {
            console.log(data);
        },

        beautify: function () {
            this.style.set("value", json.stringify(json.parse(this.style.get("value")), undefined, 4));
        }
    });
});
