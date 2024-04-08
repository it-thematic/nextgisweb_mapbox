define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    // resource
    "@nextgisweb/pyramid/i18n!",
//    "@nextgisweb/file-upload",
    "ngw-resource/serialize",
    // template
    "dojo/text!./template/Widget.hbs",
    // template
    "dijit/layout/ContentPane",
    "dojox/layout/TableContainer"
], function (
    declare,
    lang,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    i18n,
//    fileUpload,
    serialize,
    template,
    ContentPane,
    TableContainer  
) {
    return declare(
    [
        ContentPane,
        _WidgetBase,
        _TemplatedMixin,
        _WidgetsInTemplateMixin,
        serialize.Mixin
    ], {
        title: i18n.gettext("Glyphs"),
        templateString: i18n.renderTemplate(template),
        prefix: "mapbox_glyphs",

        serializeInMixin: function (data) {
            var prefix = this.prefix,
                setObject = function (key, value) { lang.setObject(prefix + "." + key, value, data); };

            setObject("glyphs", this.wGlyphs.get("value"));
        },

        validateDataInMixin: function (errback) {
            return this.composite.operation == "create" ?
                this.wGlyphs.upload_promise !== undefined &&
                    this.wGlyphs.upload_promise.isResolved() : true;
        }

    });
});
