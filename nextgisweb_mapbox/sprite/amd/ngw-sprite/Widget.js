define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "@nextgisweb/pyramid/i18n!",
//    "@nextgisweb/file-upload/file-uploader",
    "ngw-resource/serialize",
    // resource
    "dojo/text!./template/Widget.hbs",
    // template
    "dojox/layout/TableContainer",
], function (
    declare,
    lang,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    i18n,
//    fileUploader,
    serialize,
    template
) {
    return declare(
    [

        _WidgetBase, 
        _TemplatedMixin, 
        _WidgetsInTemplateMixin,
        serialize.Mixin
    ], {
        title: i18n.gettext("Sprite"),
        templateString: i18n.renderTemplate(template),
        prefix: "mapbox_sprite",

        serializeInMixin: function (data) {
            var prefix = this.prefix,
                setObject = function (key, value) { lang.setObject(prefix + "." + key, value, data); };

            setObject("sprite", this.wSprite.get("value"));
        },

        validateDataInMixin: function (errback) {
//            return this.composite.operation == "create" ?
//                this.wSprite.upload_promise !== undefined &&
//                    this.wSprite.upload_promise.isResolved() : true;
        }

    });
});
