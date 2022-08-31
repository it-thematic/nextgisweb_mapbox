define([
    "dojo/_base/declare",
    "openlayers/ol",
    "@nextgisweb/pyramid/api",
    "ngw-webmap/Adapter",
    "./MVT"
], function (
    declare,
    ol,
    api,
    Adapter,
    MVT
) {
    return declare(Adapter, {
        createLayer: function (item) {
            return new MVT(item.id, {
                visible: item.visibility,
                maxResolution: item.maxResolution ? item.maxResolution : undefined,
                minResolution: item.minResolution ? item.minResolution : undefined,
                opacity: item.transparency ? (1 - item.transparency / 100) : 1.0,
                renderMode: 'vector'
            }, {
                format: new ol.format.MVT(),
                url: api.routeURL('feature_layer.mvt') + "?z={z}&x={x}&y={y}" + "&resource=" + item.layerId
            });
        }
    });
});
