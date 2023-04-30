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

  return (
    <div className='aboutContainer'>
      <Navbar />
      <div className="aboutTitle">Analysis Result of {molecule.name} ({molecule.formula})</div>
      <div className="aboutHeroContainer">
        <div className='aboutLeft'>
          {/* <MoleculeCanvas moleculeGltfPath="./Perseverance.gltf" /> */}
          <iframe title={molecule.formula} style={{ background: "transparent" }} className='moleculeModel' frameBorder="0" src={molecule.threeDPath}></iframe>
        </div>
        <div className="aboutRight">
          {/* <div className="aboutTitle">Analysis Result of {molecule.name} ({molecule.formula})</div> */}
          <div className="aboutDescription" style={{ textAlign: "justify" }}>
            {/* The engineering physics branch's departmental club is Team Abraxas - a vibrant community of individuals fueled by passion, creativity, and technology. We embark on a journey to unravel the secrets of the universe, while at the same time, creating technological wonders that defy imagination. Our research encompasses a kaleidoscope of physics disciplines - from the frontier of quantum computing to the timeless theories of particle physics. Physics enthusiasts, come and join us in a world of discovery, where the universe is your playground and knowledge is your compass. Let's ignite your curiosity, spark new ideas and demonstrate your expertise. With discussions, demonstrations, and discoveries, we will create a captivating atmosphere that will leave a lasting impression on all who join us. Though we may be new, we are determined to make our mark and leave a legacy that will be remembered for years to come. */}
            { molecule.formula === 'H2' && <img className='resultPlot' src={plot_H2} alt="Plot of H2" /> }
            {molecule.formula === 'LiH' && <img className='resultPlot' src={plot_LiH} alt="Plot of LiH" />}
            {molecule.formula === 'BeH2' && <img className='resultPlot' src={plot_BeH2} alt="Plot of BeH2" />}
          </div>
        </div>
      </div>
      <Carousel activeMolecule={activeMolecule} handleMoleculeChange={handleChange} />
    </div>
  )
}

export default Home
