import Image from 'next/image'
import React from 'react'

const HeroSection = () => {
  return (
    <div className='px-2 container mx-auto my-5 w-full h-auto md:h-[800px]'>
      <Image
        src='/images/hero-image.jpeg'
        alt='Hero Image'
        width={1920}
        height={1000}
        className='w-full h-full object-fit'
      />
    </div>
  )
}

export default HeroSection
