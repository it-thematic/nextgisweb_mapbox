define([
    "dojo/_base/declare",
    "ngw-webmap/ol/layer/_Base"
], function (
    declare,
    _Base
) {
    return declare([_Base], {
        olLayerClassName: "layer.VectorTile",
        olSourceClassName: "source.VectorTile",

        constructor: function(name, loptions, soptions) {
            this.inherited(arguments);
        }
    });
});
