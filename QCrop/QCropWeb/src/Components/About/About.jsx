import React from 'react';
import '../../styles/about/about.css';
// import MoleculeCanvas from '../Molecule';
import Navbar from '../Navbar';
import TeamQCrop from '../../assets/images/TeamQCrop.jpg';

const About = () => {
  
  return (
    <div className='aboutContainer'>
      <Navbar />
      <div className="aboutHeroContainer">
        <div className='aboutLeft'>
                {/* <MoleculeCanvas /> */}
                <img src={TeamQCrop} alt="Team QCrop" width="500" height="500" />
        </div>
        <div className="aboutRight">
            <div className="aboutTitle">About This Project</div>
            <div className="aboutDescription" style={{textAlign:"justify"}}>
            We use Quantum Computing for Simulating Molecular Engineering for Fertilizer Design.
            </div>
        </div>
      </div>
    </div>
  )
}

export default About
