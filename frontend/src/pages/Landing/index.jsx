import Header from "../../components/Header";
import Footer from "../../components/Footer";
import CourseCatalog from "./sections/CourseCatalog";

export default function Landing(){
    return(
        <div className ="
            h-screen
            grid
            grid-rows-[1fr_10fr_1fr]
            gap-2
        ">
            <Header />

            <div className="
                border-2 rounded
                m-0.5
                ">
                    <CourseCatalog />
            </div>

            <Footer />
            
        </div>
    );
}