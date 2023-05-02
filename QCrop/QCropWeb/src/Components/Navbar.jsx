import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/navbar.css';
import QCropLogo from '../assets/images/qcropLogo.png';
import MenuIcon from '../assets/images/navbar/menu-icon.png';
import MenuCross from '../assets/images/navbar/menu-cross.png';

const Navbar = () => {

    const [sticky, setSticky] = useState(false);

    const [show, setShow] = useState("block");

    const handleShow = () => {
        document.getElementsByClassName("desktopNavbar")[0].style.display = show;
        setShow("none");
    }

    const handleHide = () => {
        document.getElementsByClassName("desktopNavbar")[0].style.display = show;
        setShow("block");
    }

    useEffect(() => {
        const handleScroll = () => {
            setSticky(window.scrollY > 200)
        }
        window.addEventListener('scroll', handleScroll)
        return () => {window.removeEventListener('scroll', handleScroll)}
    })
    return (
        <div className={`${sticky ? 'sticky' : ''} main-container`}>
            <div className="navbar">
                <div className="links">
                    <Link to='/'><img src={QCropLogo} alt='Abraxas Logo' className='logo' /></Link>
                </div>
                <img src={MenuIcon} alt="Menu Icon" width={35} className='menuIcon' onClick={() => handleShow()} />
                <div className='desktopNavbar'>
                <img src={MenuCross} alt="Menu Cross" width={50} className='menuCross' onClick={() => handleHide()} />
                    <ul className="list">
                        <li className="listItem"><Link to="/">Home</Link></li>
                        <li className="listItem"><Link to='/about'>About</Link></li>
                    </ul>
                    
                </div>
                
            </div>
        </div>
    )
}

export default Navbar;