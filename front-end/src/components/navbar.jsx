import React from 'react'
import { useState } from 'react'
import DownloadButton from './csvButton'
const Navbar = () => {
    
  return (
    <div className='flex items-center flex-row justify-between p-[20px] w-[100vw] px-[10vw] border-b-2'>
        <div className='tracking-wide'>
            <span className="mr-4 font-bold text-[22px] tracking-wide">Broker <span className='text-[#FF6B00] tracking-wide'>AI</span></span> 
        </div>
        < DownloadButton/>
    </div>

  )
}

export default Navbar