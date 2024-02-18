import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
	Sheet,
	SheetClose,
	SheetContent,
	SheetDescription,
	SheetFooter,
	SheetHeader,
	SheetTitle,
	SheetTrigger,
} from "@/components/ui/sheet"
import NeighborhoodsInfo from "./neighborhoods-info"

export function SheetDemo() {
	return (
		<Sheet>
			<SheetTrigger asChild>
				<Button variant="outline">Open</Button>
			</SheetTrigger>

			<SheetContent className="overflow-y-scroll h-full">
				<SheetClose>hello</SheetClose><NeighborhoodsInfo />
			</SheetContent>
		</Sheet>
	)
}

