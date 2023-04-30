import React, { useRef, useEffect, useState } from 'react';
import "../../styles/home/carousel.css";
import { motion } from "framer-motion";
import MoleculesList from '../../assets/data/MoleculesList.json';

const Carousel = ({ activeMolecule, handleMoleculeChange }) => {
    let Members = MoleculesList;

    const [width, setWidth] = useState(0);
    const carouselRef = useRef();

    useEffect(() => {
        setWidth(carouselRef.current.scrollWidth - carouselRef.current.offsetWidth);
    }, []);
 
    return (
        <>
            <motion.div className="carousel" ref={carouselRef}>
                <motion.div drag="x" dragConstraints={{ right:0, left: -width }} className="innerCarousel">
                    {
                        Members && Members.map((member, index) => {
                            return (
                                <motion.div className={member.formula === activeMolecule ? `card activeMoleculeCard` : `card`} key={index}>
                                    <div className='cardContent' 
                                        onClick={(e) => {
                                            e.preventDefault();
                                            handleMoleculeChange(member.formula);
                                        }}
                                    >
                                        {member.formula}
                                    </div>
                                </motion.div>
                            )
                        })
                    }
                </motion.div>
            </motion.div>
        </>
    )
}

export default Carousel
