import ChatBotSection from '@/components/ChatBotSection'
import Footer from '@/components/Footer'
import Header from '@/components/Header'
import HeroSection from '@/components/HeroSection'
import ImageUploader from '@/components/ImageUploader'
import Image from 'next/image'

export default function Home() {
  return (
    <div>
      <Header />
      <HeroSection />
      <ImageUploader />
      <ChatBotSection />
      <Footer />
    </div>
  )
}
