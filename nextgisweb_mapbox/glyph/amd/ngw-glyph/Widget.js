define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/layout/ContentPane",
    "ngw-pyramid/i18n!glyph",
    "ngw-pyramid/hbs-i18n",
    "ngw-resource/serialize",
    // resource
    "dojo/text!./template/Widget.hbs",
    // template
    "dojox/layout/TableContainer",
    "ngw-file-upload/Uploader"
], function (
    declare,
    lang,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    ContentPane,
    i18n,
    hbsI18n,
    serialize,
    template
) {
    return declare([ContentPane, serialize.Mixin, _TemplatedMixin, _WidgetsInTemplateMixin], {
        templateString: hbsI18n(template, i18n),
        title: i18n.gettext("Mapbox glyph"),
        prefix: "mapbox_glyph",

        serializeInMixin: function (data) {
            var prefix = this.prefix,
                setObject = function (key, value) { lang.setObject(prefix + "." + key, value, data); };

            setObject("sprite", this.wGlyph.get("value"));
        },

        validateDataInMixin: function (errback) {
            return this.composite.operation == "create" ?
                this.wGlyph.upload_promise !== undefined &&
                    this.wGlyph.upload_promise.isResolved() : true;
        }

    });
});