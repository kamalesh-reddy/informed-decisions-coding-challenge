import React, { useEffect, useRef} from 'react';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import decoded from './decode';

const MapComponent = () => {

  const mapRef = useRef(null);

  useEffect(() => {
    if (mapRef.current) {
      mapRef.current = L.map('map').setView([-25.2744, 133.775], 5);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; OpenStreetMap contributors'
      }).addTo(mapRef.current);
    }

    const polygons = L.featureGroup().addTo(mapRef.current);
    fetch("http://geo-exercise.id.com.au/api/geo")
    .then(response => response.json())
    .then(polygonData => {
      fetch("http://geo-exercise.id.com.au/api/data")
        .then(response=> response.json())
        .then(polygonStyles => {
          const shapeData = polygonData.shapes.map(shape => {
            const decodedPoints = decoded(shape.points);
            return {id:shape.id, points: decodedPoints};
          });

          const styleData = polygonStyles.data.reduce((result, style) => {
            const geoID = style.GeoID;
            result[geoID] = {color: style.color, infoBox: style.InfoBox};
            return result;
          }, {})

          shapeData.forEach((shape)=>{
            const polygon = L.polygon(shape.points, {color: 'black', fillColor: styleData[shape.id].color, weight: 1, opacity: 1.0, fillOpacity:1.0});
            const infoBoxData = styleData[shape.id].infoBox;
            polygon.bindTooltip(JSON.stringify(infoBoxData));
            polygons.addLayer(polygon);
          })
          
          const bounds = polygons.getBounds();
          if (bounds.isValid()) {
            mapRef.current.fitBounds(bounds);
          } 
        })
    })

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
      }
    };
  }, []);

 

  return (
    <React.Fragment>
      <div ref={mapRef} id="map" style={{ height: '100vh', width: '100%', zIndex: 0}}></div>
    </React.Fragment>
  )

 

};

 

export default MapComponent;