import L from 'leaflet';
const decoded = (encoded) => {    
    var len = String(encoded).length;
    var index = 0;
    var ar = [];
    var lat = 0;
    var lng = 0;

    try {
        while (index < len) {
            var b;
            var shift = 0;
            var result = 0;
            do {
                b = encoded.charCodeAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            }
            while (b >= 0x20);

            var dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
            lat += dlat;

            shift = 0;
            result = 0;
            do {
                b = encoded.charCodeAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            }
            while (b >= 0x20);

            var dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
            lng += dlng;

            ar.push(L.latLng((lng * 1e-5), (lat * 1e-5)));
        }
    } catch (ex) {
        //error in encoding.
    }
    return ar;
}

export default decoded;