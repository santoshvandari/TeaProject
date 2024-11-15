'use client'
import React, { useState } from 'react'

const ImageUploader = () => {
  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(false)

  const [result, setResult] = useState({
    disease: '',
    accuracy: '',
    message: '',
  })

  const handleImageChange = (e) => {
    setImage(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!image) {
      alert('Please select an image to upload.')
      return
    }
    setLoading(true)

    const formData = new FormData()
    formData.append('file', image)

    try {
      const response = await fetch('http://localhost:8000/predict/', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      if (data && data.length > 0) {
        if (response.ok) {
          setResult({
            disease: data[0].class,
            accuracy: data[0].confidence,
            message: data[0].summary,
          })
        }
      } else {
        setResult({
          disease: 'None',
          accuracy: '0',
          message: 'No Disease Detected.',
        })
      }
      setLoading(false)
    } catch (error) {
      console.error('Error uploading image:', error)
    }
  }
  return (
    <div className='grid md:grid-cols-2 gap-4 container mx-auto px-2'>
      <div>
        <h1 className='text-3xl font-bold my-10'>
          Upload Image for Disease Detection
        </h1>
        <form onSubmit={handleSubmit}>
          <div className='flex flex-col md:flex-row items-center  gap-5'>
            <label
              for='uploadFile1'
              className='bg-white text-gray-500 font-semibold text-base rounded max-w-2xl px-4 h-64 flex flex-col items-center justify-center cursor-pointer border-2 border-gray-300 border-dashed  font-[sans-serif]'
            >
              <svg
                xmlns='http://www.w3.org/2000/svg'
                className='w-11 mb-2 fill-gray-500'
                viewBox='0 0 32 32'
              >
                <path
                  d='M23.75 11.044a7.99 7.99 0 0 0-15.5-.009A8 8 0 0 0 9 27h3a1 1 0 0 0 0-2H9a6 6 0 0 1-.035-12 1.038 1.038 0 0 0 1.1-.854 5.991 5.991 0 0 1 11.862 0A1.08 1.08 0 0 0 23 13a6 6 0 0 1 0 12h-3a1 1 0 0 0 0 2h3a8 8 0 0 0 .75-15.956z'
                  data-original='#000000'
                />
                <path
                  d='M20.293 19.707a1 1 0 0 0 1.414-1.414l-5-5a1 1 0 0 0-1.414 0l-5 5a1 1 0 0 0 1.414 1.414L15 16.414V29a1 1 0 0 0 2 0V16.414z'
                  data-original='#000000'
                />
              </svg>
              Upload file
              <input
                type='file'
                id='uploadFile1'
                className='hidden'
                onChange={handleImageChange}
              />
              <p className='text-xs font-medium text-gray-400 mt-2'>
                PNG, JPG SVG, WEBP, and GIF are Allowed.
              </p>
            </label>

            <div className='flex flex-col items-center justify-center'>
              {image && (
                <img
                  src={URL.createObjectURL(image)}
                  alt='Uploaded Image'
                  className='w-full h-64 object-cover'
                />
              )}
            </div>
          </div>
          <button
            type='submit'
            className='max-w-xl w-full mt-5 bg-blue-500 text-white font-semibold text-base rounded px-4 py-2'
          >
            Submit
          </button>
        </form>

        <div className='mt-10'>
          <h2 className='text-xl font-semibold'>Instructions:</h2>
          <ul className='list-disc list-inside mt-2'>
            <li>Click on the upload file button to select an image.</li>
            <li>Click on the submit button to upload the image.</li>
          </ul>

          <h2 className='text-xl font-semibold mt-5'>Note:</h2>
          <p className='mt-2'>
            The uploaded image will be used to detect diseases in plants.
          </p>

          <p className='mt-2'>
            The output will be displayed on the screen after the image is
            uploaded.
          </p>
        </div>
      </div>
      <div className='mt-10'>
        {/* <h2 className='text-xl font-semibold'>Output:</h2> */}
        <h1 className='text-3xl font-bold my-10'>Output</h1>

        {loading && <p className='mt-2'>Loading...</p>}

        {!loading && result?.message && (
          <div className='bg-gray-100 p-4 rounded'>
            <h2 className='text-xl font-semibold'>Disease Detected:</h2>
            <p>{result?.disease}</p>

            <h2 className='text-xl font-semibold mt-5'>Accuracy:</h2>
            <p>{(result?.accuracy * 100).toFixed(2)}%</p>

            <h2 className='text-xl font-semibold mt-5'>Summary:</h2>
            {/* render html */}
            <span dangerouslySetInnerHTML={{ __html: result.message }}></span>
          </div>
        )}
      </div>
    </div>
  )
}

export default ImageUploader
