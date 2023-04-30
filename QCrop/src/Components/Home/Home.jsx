import React, { useState } from 'react'
import '../../styles/home/home.css';
// import MoleculeCanvas from '../Molecule';
import Navbar from '../Navbar';
import Carousel from './Carousel';
import MoleculesList from '../../assets/data/MoleculesList.json';

import plot_H2 from '../../assets/results/Plot_H2.png';
import plot_LiH from '../../assets/results/Plot_LiH.png';
import plot_BeH2 from '../../assets/results/Plot_BeH2.png';

const Home = () => {

  let [activeMolecule, setActiveMolecule] = useState("H2");
  let Members = MoleculesList;
  let molecule = Members.filter((molecule) => {
    return molecule.formula === activeMolecule;
  })[0]

  const handleChange = (newValue) => {
    setActiveMolecule(newValue);
  }

  // DROPDOWN
  const data = [
    {
      id: 0, label: "0.5", 
      vqeResult: -7.50392, 
      exactEnergy: -7.50400 
    }, 
    {
      id: 1, label: "0.7", 
      vqeResult: -7.04751, 
      exactEnergy: -7.04791 
    },
    {
      id: 2, label: "0.9", 
      vqeResult: -7.72278, 
      exactEnergy: -7.72283 
    },
    {
      id: 3, label: "1.1", 
      vqeResult: -7.82516, 
      exactEnergy: -7.82520
    },
    {
      id: 4, label: "1.3", 
      vqeResult: -7.86886, 
      exactEnergy: -7.86890
    },
    {
      id: 5, label: "1.5", 
      vqeResult: -7.88210, 
      exactEnergy: -7.88214
    },
    {
      id: 6, label: "1.7", 
      vqeResult: -7.87917, 
      exactEnergy: -7.87920 
    },
    {
      id: 7, label: "1.9", 
      vqeResult: -7.86788, 
      exactEnergy: -7.86799
    },
    {
      id: 8, label: "2.1", 
      vqeResult: -7.85312, 
      exactEnergy: -7.85320 
    },
    {
      id: 9, label: "2.3", 
      vqeResult: -7.83763, 
      exactEnergy: -7.83772
    },
    {
      id: 10, label: "2.5", 
      vqeResult: -7.82324, 
      exactEnergy: -7.82343
    },
    {
      id: 11, label: "2.7", 
      vqeResult: -7.81116, 
      exactEnergy: -7.81142
    },
    {
      id: 12, label: "2.9", 
      vqeResult: -7.80195, 
      exactEnergy: -7.80215 
    },
    {
      id: 13, label: "3.1", 
      vqeResult: -7.79516, 
      exactEnergy: -7.79545
    },
    {
      id: 14, label: "3.3", 
      vqeResult: -7.78973, 
      exactEnergy: -7.79085
    },
    {
      id: 15, label: "3.5", 
      vqeResult: -7.78572, 
      exactEnergy: -7.78776
    },
    {
      id: 16, label: "3.7", 
      vqeResult: -7.78351, 
      exactEnergy: -7.78573
    },
    {
      id: 17, label: "3.9", 
      vqeResult: -7.78245, 
      exactEnergy: -7.78441
    }
  ];

  const [isOpen, setOpen] = useState(false);
  const [items, setItem] = useState(data);
  const [selectedItem, setSelectedItem] = useState(null);
  
  const toggleDropdown = () => setOpen(!isOpen);
  
  const handleItemClick = (id) => {
    selectedItem === id ? setSelectedItem(null) : setSelectedItem(id);
  }

  return (
    <div className='aboutContainer'>
      <Navbar />
      <div className='moleculeCarousel'>
        <Carousel activeMolecule={activeMolecule} handleMoleculeChange={handleChange} />
      </div>
      <div className="resultTitle">Analysis Result of {molecule.name} ({molecule.formula})</div>
      <div className="aboutHeroContainer">
        <div className='aboutLeft'>
          {/* <MoleculeCanvas moleculeGltfPath="./Perseverance.gltf" /> */}
          <iframe title={molecule.formula} style={{ background: "transparent" }} className='moleculeModel' frameBorder="0" src={molecule.threeDPath}></iframe>
        </div>
        <div className="aboutRight">
          {/* <div className="aboutTitle">Analysis Result of {molecule.name} ({molecule.formula})</div> */}
          <div className="aboutDescription" style={{ textAlign: "justify" }}>
            {/* The engineering physics branch's departmental club is Team Abraxas - a vibrant community of individuals fueled by passion, creativity, and technology. We embark on a journey to unravel the secrets of the universe, while at the same time, creating technological wonders that defy imagination. Our research encompasses a kaleidoscope of physics disciplines - from the frontier of quantum computing to the timeless theories of particle physics. Physics enthusiasts, come and join us in a world of discovery, where the universe is your playground and knowledge is your compass. Let's ignite your curiosity, spark new ideas and demonstrate your expertise. With discussions, demonstrations, and discoveries, we will create a captivating atmosphere that will leave a lasting impression on all who join us. Though we may be new, we are determined to make our mark and leave a legacy that will be remembered for years to come. */}
            {molecule.formula === 'H2' && <img className='resultPlot' src={plot_H2} alt="Plot of H2" />}
            {molecule.formula === 'LiH' && <img className='resultPlot' src={plot_LiH} alt="Plot of LiH" />}
            {molecule.formula === 'BeH2' && <img className='resultPlot' src={plot_BeH2} alt="Plot of BeH2" />}
          </div>
        </div>
      </div>
      {
        // molecule.formula === 'H2' &&
        <div className="dataDiv">
          <div className='dropdown'>
            <div className='dropdown-header' onClick={toggleDropdown}>
              {selectedItem ? items.find(item => item.id === selectedItem).label : "Select Interatomic Distance"}
              <i className={`fa fa-chevron-right icon ${isOpen && "open"}`}></i>
            </div>
            <div className={`dropdown-body ${isOpen && 'open'}`}>
              {items.map(item => (
                <div className="dropdown-item" onClick={e => handleItemClick(e.target.id)} id={item.id}>
                  <span className={`dropdown-item-dot ${item.id === selectedItem && 'selected'}`}>• </span>
                  {item.label}
                </div>
              ))}
            </div>
          </div>
          <div className="vqeRes">
            VQE Result: {selectedItem ? `${selectedItem.vqeResult}` : ''}
          </div>
          <div className="exactEnergy">
            Exact Energy: {selectedItem ? `${selectedItem.exactEnergy}` : ''}
          </div>
        </div>
      }
    </div>
  )
}

export default Home
