import React from "react";
// import { useQuery } from "react-query";
import data from "./data.json";

import {
  Popup,
  Marker,
  LayersControl,
  TileLayer,
  MapContainer,
  FeatureGroup,
  Circle,
  LayerGroup,
  Rectangle,
} from "react-leaflet";
import ShowCrimes from "./ShowPeopleNeeds";
const center = [24.466667, 54.366669];
const rectangle = [
  [51.49, -0.08],
  [51.5, -0.06],
];
function Map() {
  // const { isLoading, error, data } = useQuery("repoData", () =>
  //   fetch("./data.json").then((res) => res.json())
  // );

  // if (isLoading) return "Loading...";

  // if (error) return "An error has occurred: " + error.message;

  console.log(data);

  return (
    <MapContainer center={[24.466667, 54.366669]} zoom={13} scrollWheelZoom={false}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
      <ShowCrimes data={data} />
      <LayersControl position="topright">
        <LayersControl.Overlay name="Marker with popup">
          <Marker position={center}>
            <Popup>
              A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
          </Marker>
        </LayersControl.Overlay>
        <LayersControl.Overlay checked name="Layer group with circles">
          <LayerGroup>
            <Circle center={center} pathOptions={{ fillColor: "blue" }} radius={200} />
            <Circle
              center={center}
              pathOptions={{ fillColor: "red" }}
              radius={100}
              stroke={false}
            />
            <LayerGroup>
              <Circle
                center={center}
                pathOptions={{ color: "green", fillColor: "green" }}
                radius={100}
              />
            </LayerGroup>
          </LayerGroup>
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Feature group">
          <FeatureGroup pathOptions={{ color: "purple" }}>
            <Popup>Popup in FeatureGroup</Popup>
            <Circle center={center} radius={200} />
            <Rectangle bounds={rectangle} />
          </FeatureGroup>
        </LayersControl.Overlay>
      </LayersControl>
    </MapContainer>
  );
}

export default Map;
