import React, { useEffect } from 'react';
import { getCoursePreviews } from '../../../services/courseService';

function CourseCard({ coursePreview }){
    return(
        <div className="
            border-2 rounded
            p-2
            ">
            <h2>{coursePreview.title}</h2>
            <p>{coursePreview.description}</p>
            <p>{coursePreview.description}</p>
            <ul>
                {coursePreview.tags_main.map((tag, index) => (
                    <li key={index}>{tag}</li>
                ))}
            </ul>
            <p>{coursePreview.resource_count}</p>
            <p>{coursePreview.video_duration}</p>
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
            grid-rows-[auto_1fr]
            gap-2
            p-2
        ">
            <h2> Catálogo </h2>
            <div className="
                grid
                grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4
                h-full
                gap-2
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