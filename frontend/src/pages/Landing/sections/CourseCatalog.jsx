import React, { useEffect } from 'react';
import { getCoursePreviews } from '../../../services/courseService';

function CourseCard({ coursePreview }){
    return(
        <div className="
            relative
            w-full
            md:aspect-[5/3]
            sm:aspect-[4/2]
            mt-16
        ">
            <div className="absolute -top-20 left-5  
                            md:w-40 md:h-40  
                            sm:w-32 sm:h-32
                            w-24 h-24
                            rounded-full bg-white border-2 border-black overflow-hidden 
                            shadow-[2px_2px_1px_1px_rgba(0,0,0,0.5)] bg-[url('/prueba.webp')] bg-cover bg-center">
            </div>
            <div className="border-2 rounded-2xl h-full shadow-[4px_4px_1px_1px_rgba(0,0,0,0.5)] p-2 flex flex-col absolute-inset-0">
                <header className="pt-2 pr-2">
                    <h3 className="text-right text-xl sm:text-2xl font-semibold tracking-tight leading-snug">
                        {coursePreview.title}
                    </h3>
                </header>
                <section className=" mt-10 ml-2 overflow-auto">
                    <p className="text-sm sm:text-base text-gray-700 leading-relaxed">
                        {coursePreview.description}
                    </p>
                    <p className ="mt-1">
                        {coursePreview.tags_main.slice(0, 3).map((tag, index) => (
                            <span key={index} className="inline-block px-2 py-0.5 mr-2 rounded-full border border-black/20 bg-black/5 last:mr-0">
                                {tag}
                            </span>
                        ))}
                    </p>
                    <p>{coursePreview.resource_count}</p>
                    <p>{coursePreview.video_duration}</p>
                </section>
            </div>            
        </div>
    )
}

export default function CourseCatalog(){
    const [coursePreviews, setCoursePreviews] = React.useState([]);

    useEffect(() => {
        getCoursePreviews()
            .then(data => setCoursePreviews(data))
            .catch(error => console.error('Error fetching course previews:', error))
    }, []);
    return(
        <section className="
            h-full
            grid
            grid-rows-[1fr_12fr]
            gap-2
            p-2
        ">
            <div><h2> Catálogo </h2></div>
            <div className="
                grid
                grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4
                h-full
                gap-8
                m-0.5
                ">
                {
                    coursePreviews.map((CoursePreview) => (
                        <CourseCard key={CoursePreview.id} coursePreview={CoursePreview} />
                        )
                    )
                }                
            </div>
        </section>
    )
}