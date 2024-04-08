/* globals define, console */
define([
    "dojo/_base/declare",
    "dojo/aspect",
    "dojo/json",
    "dojo/request/xhr",
    "dijit/layout/ContentPane",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "ngw-pyramid/route",
    "ngw-resource/ResourceBox",
    "@nextgisweb/pyramid/i18n!",
    "ngw-resource/serialize",
    "dojo/text!./template/Widget.hbs",
    // template
    "dijit/form/Textarea",
    "dijit/Dialog",
    "dijit/layout/BorderContainer",
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
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    route,
    ResourceBox,
    i18n,
    serialize,
    template
) {
    return declare(
    [
        ContentPane,
        _WidgetBase, 
        _TemplatedMixin, 
        _WidgetsInTemplateMixin,
        serialize.Mixin
    ], {
        title: i18n.gettext("Mapbox style"),
        templateString: i18n.renderTemplate(template),
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
