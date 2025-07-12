// Timeline data for the photo journey
const timelineData = [
    {
        id: 1,
        year: 2012,
        month: "Summer",
        title: "Early Adventures",
        description: "Our first adventures together - exploring the city and making memories with friends.",
        images: [
            {
                src: "https://storage.googleapis.com/wedding-website-2025-regdev-1752188684/earlydays_group_fun1.jpg",
                alt: "Party on the Boat",
                title: "Party on the Boat",
                description: "Unforgettable fun and laughter with friends on the water"
            },
            {
                src: "https://storage.googleapis.com/wedding-website-2025-regdev-1752188684/earlydays_group_fun2.jpg",
                alt: "Laughs with Friends",
                title: "Laughs with Friends", 
                description: "Cherished moments and big smiles from our early days together"
            },
            {
                src: "https://storage.googleapis.com/wedding-website-2025-regdev-1752188684/earlydays_lakeigha_pose.jpg",
                alt: "Lakeigha in the City",
                title: "Lakeigha in the City",
                description: "Lakeigha striking a pose in the city during our early adventures"
            }
        ],
        icon: "🌅",
        color: "from-blue-400 to-purple-500"
    },
    {
        id: 2,
        year: 2023,
        month: "Spring",
        title: "Growing Together",
        description: "Building our life together, embracing new adventures and creating our own traditions.",
        images: [
            {
                src: "./images/jeep_life_red.jpg",
                alt: "Jeep Adventures",
                title: "Jeep Adventures",
                description: "Our love for adventure and the open road"
            },
            {
                src: "./images/vacation_swimsuit.jpg",
                alt: "Vacation Vibes",
                title: "Vacation Vibes",
                description: "Relaxing together in paradise"
            }
        ],
        icon: "🌱",
        color: "from-green-400 to-blue-500"
    },
    {
        id: 3,
        year: 2024,
        month: "Summer",
        title: "The Proposal",
        description: "The moment that changed everything - when we decided to spend forever together. A magical vacation that became the beginning of forever.",
        images: [
            {
                src: "https://storage.googleapis.com/wedding-website-2025-regdev-1752188684/proposal-vacay.png",
                alt: "Proposal Vacation",
                title: "Another Proposal Moment",
                description: "One of the many moments Marcus asked Lakeigha to spend forever together."
            }
        ],
        video: {
            src: "./videos/proposal.mp4",
            title: "The Proposal Video",
            description: "Watch the magical moment when Marcus asked Lakeigha to spend forever together",
            duration: "2:34",
            featured: true
        },
        icon: "💍",
        color: "from-pink-400 to-red-500"
    },
    {
        id: 4,
        year: 2024,
        month: "Fall",
        title: "Professional Memories",
        description: "Capturing our love story through the lens of a professional photographer.",
        images: [
            {
                src: "./images/proshot.jpg",
                alt: "Professional Love",
                title: "Professional Love",
                description: "Our official engagement photos"
            }
        ],
        icon: "📸",
        color: "from-purple-400 to-pink-500"
    },
    {
        id: 5,
        year: 2024,
        month: "Fall",
        title: "Making It Official",
        description: "Taking the next step in our journey together.",
        images: [
            {
                src: "./images/marriage-license.jpg",
                alt: "The Big Step",
                title: "The Big Step",
                description: "Making it official - our marriage license"
            }
        ],
        icon: "📜",
        color: "from-yellow-400 to-orange-500"
    },
    {
        id: 6,
        year: 2025,
        month: "Present",
        title: "Celebrating Love",
        description: "Embracing our Texas roots and celebrating our love story.",
        images: [
            {
                src: "./images/champ-keke-red-black.jpg",
                alt: "Champagne Celebration",
                title: "Champagne Celebration",
                description: "Celebrating our love with style and elegance"
            },
            {
                src: "./images/cowboy_beige_white.jpg",
                alt: "Cowboy Style",
                title: "Cowboy Style",
                description: "Embracing our Texas roots"
            }
        ],
        icon: "🤠",
        color: "from-red-400 to-pink-500"
    }
];

// Timeline utility functions
const timelineUtils = {
    // Get timeline data
    getTimelineData() {
        return timelineData;
    },
    
    // Get timeline item by ID
    getTimelineItem(id) {
        return timelineData.find(item => item.id === id);
    },
    
    // Get all images from timeline
    getAllImages() {
        return timelineData.flatMap(item => 
            item.images.map(img => ({
                ...img,
                timelineItem: item
            }))
        );
    },
    
    // Format year and month for display
    formatDate(year, month) {
        return `${month} ${year}`;
    },
    
    // Get current timeline position (for animations)
    getCurrentPosition() {
        const now = new Date();
        const weddingDate = new Date('August 8, 2025');
        const totalDuration = weddingDate.getTime() - new Date('2012-01-01').getTime();
        const elapsed = now.getTime() - new Date('2012-01-01').getTime();
        return Math.min(Math.max(elapsed / totalDuration, 0), 1);
    }
};

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.timelineData = timelineData;
    window.timelineUtils = timelineUtils;
} 