import React from 'react';
import './Hero.css';

const Hero = ({ headline, introduction, heroImage }) => {
    headline = "Welcome to CodeOwl";
    introduction = "CodeOwl is a semantic knowledge platform that unifies software development data—architectures, methodologies, and real-time GitHub insights—into a coherent RDF-based model. Effortlessly explore relationships between projects, technologies, and licenses, and discover hidden patterns to power informed decision-making in your software ecosystem. Enjoy intuitive natural language queries, a user-friendly interface, and rich, interconnected insights—all in one place.";
    heroImage = "/home.png";
  return (
    <div className="container-fluid">
      <div className="hero-wrapper row flex-md-row flex-align-items-start">
        <div className="col-md-6 col-md">
          <div className="hero__content">
            <h1 className="hero__headline text-bg">{headline}</h1>
            <h3 className="hero__text">{introduction}</h3>
          </div>
        </div>
        <div className="col-md-6" style={{'height': '120%'>
          <div className="hero__image" style={{'width': 'auto', 'height': '100%'>
            {/* inline style for width/height in React */}
            <img 
              src={heroImage} 
              alt="hero" 
              style={{ width: 'auto', height: '100%' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
